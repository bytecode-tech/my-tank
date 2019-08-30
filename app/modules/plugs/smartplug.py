from pyHS100 import Discover

def discover_plugs():
    plugs = []
    for dev in Discover.discover().values():
        if dev.is_plug:
            plugs.append(dev)
    return plugs