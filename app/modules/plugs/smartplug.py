from pyHS100 import Discover, SmartPlug

def discover_plugs():
    plugs = []
    for dev in Discover.discover().values():
        if isinstance(dev, SmartPlug):
            plugs.append(dev)
    return plugs