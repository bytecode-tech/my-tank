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
        id: str,
        alias: str,
        host: str
    ) -> None:
    
        Strip.__init__(self, id, alias, host, DeviceBrand.tp_link)
        self.native_api = SmartStrip(host)
        _LOGGER.debug(
            "Initializing tp-link smartplug: %s",
            self.host,
        )

        # self.initialize()

    def __eq__(self, obj):
        return isinstance(obj, TplinkStrip) and obj.id == self.id

    @property
    def has_integrity(self):
        try:
            deviceId = self.sys_info['deviceId']
            if deviceId.lower() == self.id:
                return True
            else:
                return False
        except:
            return False

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

    def get_is_off(self, *, index: int = -1) -> Any:
        """
        Returns whether device is off.
        :param index: plug index (-1 for all)
        :return: True if device is off, False otherwise, Dict without index
        :rtype: bool if index is provided
                Dict[int, bool] if no index provided
        :raises SmartStripException: index out of bounds
        """
        return self.native_api.get_is_off(index=index)

    @property
    def is_on(self) -> bool:
        """Return if the device is on.

        :return: True if the device is on, False otherwise.
        :rtype: bool
        :return:
        """
        return self.native_api.is_on

    def get_is_on(self, *, index: int = -1) -> Any:
        """
        Returns whether device is on.
        :param index: plug index (-1 for all)
        :return: True if device is on, False otherwise, Dict without index
        :rtype: bool if index is provided
                Dict[int, bool] if no index provided
        :raises SmartStripException: index out of bounds
        """
        return self.native_api.get_is_on(index=index)

    def turn_on(self, *, index: int = -1):
        """
        Turns outlets on
        :param index: plug index (-1 for all)
        """
        return self.native_api.turn_on(index=index)

    def turn_off(self, *, index: int = -1):
        """
        Turns outlets off
        :param index: plug index (-1 for all)
        """
        return self.native_api.turn_off(index=index)

    @property
    def children_info(self) -> Dict[int, Any]:
        info = {}
        children_on_state = self.native_api.get_is_on()
        children_alias = self.native_api.get_alias()

        for child in children_on_state:
            info[child + 1] = {'is_on': children_on_state[child], 'alias': children_alias[child]}
        
        return info

    @property
    def state_information(self) -> Dict[str, Any]:
        """Return device-type specific, end-user friendly state information.

        :return: dict with state information.
        :rtype: dict
        """
        return self.native_api.state_information


