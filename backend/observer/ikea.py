import dirigera
from dirigera.hub.abstract_smart_home_hub import AbstractSmartHomeHub
from .config import TOKEN, IP

HUB = dirigera.Hub(token=TOKEN, ip_address=IP)

# White list of device attributes to be logged
ATTRIBUTES = {
    "environmentSensor": ["currentTemperature", "currentRH", "currentPM25", "vocIndex"],
    "motionSensor": ["isOn", "isDetected", "batteryPercentage"],
    "lightSensor": ["illuminance"],
}

# Don't log these devices
NOT_IMPLEMENTED = ["gateway"]


def get_devices(hub: AbstractSmartHomeHub = HUB) -> list[dict]:
    return HUB.get(route="/devices")


def filter_attributes(type: str, attributes: dict) -> dict:
    """
    type is a key for ATTRIBUTES
    Returns subset of attributes only with the keys from ATTRIBUTES[type]
    """
    if type not in ATTRIBUTES:
        raise ValueError(f"Unknown type: {type}")
    whitelist = ATTRIBUTES[type]
    return {k: attributes[k] for k in whitelist}
