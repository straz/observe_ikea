# White list of device attributes to be logged
ATTRIBUTES = {
    "environmentSensor": ["currentTemperature", "currentRH", "currentPM25", "vocIndex"],
    "motionSensor": ["isOn", "isDetected", "batteryPercentage"],
    "lightSensor": ["illuminance"],
    "waterSensor": ["batteryPercentage", "waterLeakDetected"],
}

# Don't log these devices
NOT_IMPLEMENTED = ["gateway"]


def filter_attributes(type: str, attributes: dict) -> dict:
    """
    type is a key for ATTRIBUTES
    Returns subset of attributes only with the keys from ATTRIBUTES[type]
    """
    if type not in ATTRIBUTES:
        raise ValueError(f"Unknown type: {type}")
    whitelist = ATTRIBUTES[type]
    return {k: attributes[k] for k in whitelist if k in attributes}
