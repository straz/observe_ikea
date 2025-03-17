from __future__ import annotations
from typing import Any, ClassVar
from pydantic import BaseModel, ConfigDict, Field, computed_field
from functools import cached_property
from datetime import datetime, timezone
import requests

import dirigera
from dirigera.hub.abstract_smart_home_hub import AbstractSmartHomeHub
from .database import Database
from .get_data import log_device, log_error
from .config import HOMES


class Home(BaseModel):
    # Keep a registry of all Home instances
    _homes: ClassVar[list[Home]] = []

    name: str = "Default home"
    ip: str
    token: str = Field(exclude=True, repr=False)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field  # type: ignore[misc]
    # see https://docs.pydantic.dev/2.0/usage/computed_fields/
    @cached_property
    def hub(self) -> AbstractSmartHomeHub:
        return dirigera.Hub(token=self.token, ip_address=self.ip)

    def model_post_init(self, context: Any):
        self.__class__._homes += [self]

    def get_devices(self) -> list[dict]:
        return self.hub.get(route="/devices")

    def get_sensors(self) -> dict[str, dict[str, str]]:
        return {
            d["id"]: {'name': device_name(d), 'type': d["deviceType"]}
            for d in self.get_devices()
            if d["deviceType"] != "gateway"
        }

    @classmethod
    def init_all(cls):
        for home in HOMES:
            cls(**home)

    @classmethod
    def all_current_sensors(cls) -> dict:
        return {h.name: h.get_sensors() for h in cls._homes}

    @classmethod
    def log_all(cls):
        """
        For each Home, record all devices
        """
        now = datetime.now(timezone.utc)
        db = Database(month=now.month, year=now.year)
        for home in cls._homes:
            home.log_all_devices(db=db, now=now)

    def log_all_devices(self, db: Database, now: datetime):
        """
        Get data from the sensors connected to the IKEA DIRIGERA zigbee hub.
        Log the data into the local database.
        """
        try:
            for device in self.get_devices():
                log_device(db=db, now=now, device=device)
        except requests.exceptions.ConnectionError as err:
            log_error(db=db, now=now, event="Dirigera connection error", err=err)
        except requests.exceptions.ConnectTimeout as err:
            log_error(db=db, now=now, event="Dirigera timeout", err=err)


def device_name(device: dict) -> str:
    """
    Returns the custom name (if available), or a reasonable default.
    """
    return (
        device["attributes"]["customName"]
        or f"{device['attributes']['model']}-{device['attributes']['serialNumber']}"
    )
