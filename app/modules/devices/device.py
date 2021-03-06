import logging
import json
from typing import Any, Dict, Optional, TextIO
from enum import Enum

_LOGGER = logging.getLogger(__name__)

class DeviceType(Enum):
    """Device type enum."""

    relay = 1
    plug = 2
    strip = 3
    unkown = -1

class DeviceBrand(Enum):
    """Device brand enum."""
    onboard = 1
    tp_link = 2
    unkown = -1


class DeviceException(Exception):
    """Base exception for device errors."""

class Device:
    """Base class for all supported device types."""

    STATE_ON = "ON"
    STATE_OFF = "OFF"

    def __init__(
        self,
        id: str,
        alias: str,
        host: str,
        device_type: DeviceType = DeviceType.unkown,
        device_brand: DeviceBrand = DeviceBrand.unkown
    ) -> None:
    
        self.alias = alias
        self.host = host
        self.id = id

        _LOGGER.debug(
            "Initializing %s",
            self.host,
        )
        
        self._device_type = device_type
        self._device_brand = device_brand

    @property
    def sys_info(self) -> Dict[str, Any]:
        """Return the complete system information.

        :return: System information dict.
        :rtype: dict
        """

        return self.get_sysinfo()

    def get_sysinfo(self) -> Dict:
        """Retrieve system information.

        :return: sysinfo
        :rtype dict
        :raises SmartDeviceException: on error
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    @property
    def model(self) -> str:
        """Return device model.

        :return: device model
        :rtype: str
        :raises SmartDeviceException: on error
        """
        return str(self.sys_info["model"])

    @property
    def icon(self) -> Dict:
        """Return device icon.

        Note: not working on HS110, but is always empty.

        :return: icon and its hash
        :rtype: dict
        :raises SmartDeviceException: on error
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    @icon.setter
    def icon(self, icon: str) -> None:
        """Set device icon.

        Content for hash and icon are unknown.

        :param str icon: Icon path(?)
        :raises NotImplementedError: when not implemented
        :raises SmartPlugError: on error
        """
        raise NotImplementedError()

    def reboot(self, delay=1) -> None:
        """Reboot the device."""

        raise NotImplementedError("Device subclass needs to implement this.")

    def turn_off(self) -> None:
        """Turn off the device."""
        raise NotImplementedError("Device subclass needs to implement this.")

    @property
    def is_off(self) -> bool:
        """Return True if device is off.

        :return: True if device is off, False otherwise.
        :rtype: bool
        """
        return not self.is_on

    def turn_on(self) -> None:
        """Turn device on."""
        raise NotImplementedError("Device subclass needs to implement this.")

    def toggle(self) -> None:
        """Toggle device state"""
        self.turn_on() if self.is_off else self.turn_off()

    @property
    def is_on(self) -> bool:
        """Return if the device is on.

        :return: True if the device is on, False otherwise.
        :rtype: bool
        :return:
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    @property
    def state_information(self) -> Dict[str, Any]:
        """Return device-type specific, end-user friendly state information.

        :return: dict with state information.
        :rtype: dict
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    @property
    def has_children(self) -> bool:
        """Return if the device has children"""

        raise NotImplementedError("Device subclass needs to implement this.")

    @property
    def brand(self) -> str:
        return self._device_brand.name

    @property
    def type(self) -> str:
        return self._device_type.name

    @property
    def device_type(self) -> DeviceType:
        """Return the device type."""
        return self._device_type

    @property
    def is_gpio(self) -> bool:
        return self._device_type == DeviceType.GPIO

    @property
    def is_plug(self) -> bool:
        return self._device_type == DeviceType.plug

    @property
    def is_strip(self) -> bool:
        return self.device_type == DeviceType.strip

    def save(self, file: TextIO, fields: dict=None):
        me = { "alias": self.alias,
                "id": self.id,
                "host": self.host,
                "brand": self._device_brand.name,
                "type": self._device_type.name,
                "class": self.__class__.__name__,
            }
        if fields:
            me.update( fields )
            
        json_data = json.dumps(me)

        file.write(json_data)
        file.close()

    def __repr__(self):
        is_on = self.is_on
        if callable(is_on):
            is_on = is_on()
        return "<%s model %s at %s (%s), is_on: %s - dev specific: %s>" % (
            self.__class__.__name__,
            self.model,
            self.host,
            self.alias,
            is_on,
            self.state_information,
        )