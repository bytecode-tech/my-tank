import logging
import json
from typing import Any, Dict, TextIO
from app.gpiozeroext.output_devices import Relay

from . import (
    Device,
    DeviceType,
)

_LOGGER = logging.getLogger(__name__)

class OnboardReplay(Device):

    def __init__(
        self,
        alias: str,
        gpio: int,
    ) -> None:
    
        Device.__init__(self, alias, 'local', "onboard")
        self.gpio = gpio
        self.native_api = Relay(gpio)
        _LOGGER.debug(
            "Initializing onboard relay: %s on GPIO: %s",
            self.alias,
            gpio,
        )

        self._device_type = DeviceType.GPIO

    def turn_off(self) -> None:
        """Turn device off."""
        return self.native_api.off()

    @property
    def is_off(self) -> bool:
        """Return True if device is off.

        :return: True if device is off, False otherwise.
        :rtype: bool
        """
        return not self.is_on

    def turn_on(self) -> None:
        """Turn device on."""
        return self.native_api.on()

    @property
    def is_on(self) -> bool:
        """Return if the device is on.

        :return: True if the device is on, False otherwise.
        :rtype: bool
        :return:
        """
        return self.native_api.value

    @property
    def state_information(self) -> Dict[str, Any]:
        """Return device-type specific, end-user friendly state information.

        :return: dict with state information.
        :rtype: dict
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    def get_sysinfo(self) -> Dict:
        """Retrieve system information.

        :return: sysinfo
        :rtype dict
        :raises SmartDeviceException: on error
        """
        return { "GPIO": self.gpio}

    def save(self, file: TextIO, fields: dict=None):
        me = { 
                "gpio": self.gpio,
            }
        me.update(fields)
        return Device.save(self, file, me)

    
