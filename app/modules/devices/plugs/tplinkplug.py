import logging
from pyHS100 import SmartPlug
from typing import Any, Dict

from app.modules.devices import (
    Device,
    DeviceType,
    DeviceBrand
)

from . import (
    Plug,
)

_LOGGER = logging.getLogger(__name__)

class TplinkPlug(Plug):

    def __init__(
        self,
        id: str,
        alias: str,
        host: str
    ) -> None:
    
        Plug.__init__(self, id, alias, host, DeviceBrand.tp_link)

        self.native_api = SmartPlug(host)
        _LOGGER.debug(
            "Initializing tp-link smartplug: %s",
            self.host,
        )

        # self.initialize()

    def get_sysinfo(self) -> Dict:
        """Retrieve system information.

        :return: sysinfo
        :rtype dict
        :raises SmartDeviceException: on error
        """
        return self.native_api.sys_info

    @property
    def is_off(self) -> bool:
        """Return True if device is off.

        :return: True if device is off, False otherwise.
        :rtype: bool
        """
        return self.native_api.is_off

    def turn_on(self) -> None:
        """Turn device on."""
        return self.native_api.turn_on()

    def turn_off(self) -> None:
        """Turn device off."""
        return self.native_api.turn_off()

    @property
    def is_on(self) -> bool:
        """Return if the device is on.

        :return: True if the device is on, False otherwise.
        :rtype: bool
        :return:
        """
        try:
            return self.native_api.is_on
        except:
            return None

    @property
    def state_information(self) -> Dict[str, Any]:
        """Return device-type specific, end-user friendly state information.

        :return: dict with state information.
        :rtype: dict
        """
        return self.native_api.state_information


