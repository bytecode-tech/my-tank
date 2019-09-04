import logging
from typing import Any, Dict

from app.modules.devices import (
    Device,
    DeviceType,
)

_LOGGER = logging.getLogger(__name__)

class Plug(Device):

    def __init__(
        self,
        host: str,
        brand: str,
        model: str = None,
    ) -> None:
    
        self.host = host
        self.brand = brand
        self.model = model
        _LOGGER.debug(
            "Initializing %s",
            self.host,
        )
        self._device_type = DeviceType.Plug

        # self.initialize()

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

    def get_sysinfo(self) -> Dict:
        """Retrieve system information.

        :return: sysinfo
        :rtype dict
        :raises SmartDeviceException: on error
        """
        raise NotImplementedError("Device subclass needs to implement this.")
