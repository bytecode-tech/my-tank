import logging
from pyHS100 import SmartPlug
from typing import Any, Dict

from app.modules.devices.plugs import (
    Plug,
)

_LOGGER = logging.getLogger(__name__)

class TplinkPlug(Plug):

    def __init__(
        self,
        vendor_plug: SmartPlug,
    ) -> None:
    
        self.host = vendor_plug.host
        self.brand = "tp-link"
        self.style = "smartplug"
        self.native_api = vendor_plug
        _LOGGER.debug(
            "Initializing tp-link smartplug: %s",
            self.host,
        )

        # self.initialize()

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
        return self.native_api.is_on

    @property
    def state_information(self) -> Dict[str, Any]:
        """Return device-type specific, end-user friendly state information.

        :return: dict with state information.
        :rtype: dict
        """
        return self.native_api.state_information

