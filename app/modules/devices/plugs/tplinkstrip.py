import logging
from pyHS100 import SmartPlug, SmartStrip
from typing import Any, Dict

from app.modules.devices import (
    Device,
    DeviceType,
    DeviceBrand
)

from . import (
    Strip,
)

_LOGGER = logging.getLogger(__name__)

class TplinkStrip(Strip):

    def __init__(
        self,
        alias: str,
        host: str
    ) -> None:
    
        Strip.__init__(self, alias, host, DeviceBrand.tplink)
        self.native_api = SmartStrip(host)
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
        return not self.native_api.is_on

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
        return self.native_api.is_on

    @property
    def children_info(self) -> Dict[int, Any]:
        info = {}
        children_on_state = self.native_api.get_is_on(index=-1)
        children_alias = self.native_api.get_alias(index=-1)

        for child in children_on_state:
            info[child] = {'is_on': children_on_state[child], 'alias': children_alias[child]}
        
        return info

    @property
    def state_information(self) -> Dict[str, Any]:
        """Return device-type specific, end-user friendly state information.

        :return: dict with state information.
        :rtype: dict
        """
        return self.native_api.state_information


