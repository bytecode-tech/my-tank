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
        alias: str,
        host: str,
        brand: DeviceBrand,
    ) -> None:
    
        Device.__init__(self, alias, host, DeviceType.strip, brand)
        _LOGGER.debug(
            "Initializing %s",
            self.host,
        )

        # self.initialize()

    @property
    def has_children(self) -> bool:
        """Return if the device has children"""

        return True

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



