import logging
from typing import Any, Dict

from app.modules.devices import (
    Device,
    DeviceType,
    DeviceBrand
)

from . import Plug

_LOGGER = logging.getLogger(__name__)

class Strip(Plug):

    def __init__(
        self,
        id: str,
        alias: str,
        host: str,
        brand: DeviceBrand,
    ) -> None:
    
        Device.__init__(self, id, alias, host, DeviceType.strip, brand)
        _LOGGER.debug(
            "Initializing %s",
            self.host,
        )

        # self.initialize()

    @property
    def has_children(self) -> bool:
        """Return if the device has children"""

        return True

    def get_is_off(self, *, index: int = -1) -> Any:
        """
        Returns whether device is off.
        :param index: plug index (-1 for all)
        :return: True if device is off, False otherwise, Dict without index
        :rtype: bool if index is provided
                Dict[int, bool] if no index provided
        :raises SmartStripException: index out of bounds
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    def turn_on(self, *, index: int = -1):
        """
        Turns outlets on
        :param index: plug index (-1 for all)
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    def turn_off(self, *, index: int = -1):
        """
        Turns outlets off
        :param index: plug index (-1 for all)
        """
        raise NotImplementedError("Device subclass needs to implement this.")

    def toggle(self, *, index: int = -1) -> None:
            """Toggle device state"""
            self.turn_on(index=index) if self.get_is_off(index=index) else self.turn_off(index=index)
