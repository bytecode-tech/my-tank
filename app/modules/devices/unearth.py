import logging
from pyHS100 import Discover, SmartPlug, SmartStrip
from typing import Dict, Type, Optional

from app.modules.devices import (
    Device,
)
 
from app.modules.devices.plugs import (
    Plug,
    TplinkPlug,
    TplinkStrip,
)

_LOGGER = logging.getLogger(__name__)


class Unearth:

    @staticmethod
    def unearth(ttl_hash=None) -> Dict[str, Device]:

        devices = {}
        _LOGGER.debug("Searching for new devices...")

        try:
            for dev in Discover.discover().values():
                if isinstance(dev, SmartStrip):
                    devices[dev.alias] = TplinkStrip(dev.alias, dev.host)
                elif isinstance(dev, SmartPlug):
                    devices[dev.alias] = TplinkPlug(dev.alias, dev.host)
        except Exception as ex:
            _LOGGER.error("Got exception %s", ex, exc_info=True)
        _LOGGER.debug("Found %s devices", len(devices))
        return devices
