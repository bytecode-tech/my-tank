#!/usr/bin/python
import git
import os
from dbus import SystemBus, Interface

def updateSource():
    g = git.Git('/home/pi/zero-appliance')
    return g.pull('origin')

def checkUpdate():
    g = git.Git('/home/pi/zero-appliance')
    return g.status('-uno')

def applianceRestart():
    return os.system('sudo systemctl restart zero-appliance')

def applianceState():
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1','/org/freedesktop/systemd1')
    manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    appliance_unit = manager.LoadUnit('zero-appliance.service')
    appliance_proxy = bus.get_object('org.freedesktop.systemd1', str(appliance_unit))
    appliance_properties = Interface(appliance_proxy, dbus_interface='org.freedesktop.DBus.Properties')
    return appliance_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')

def exporterRestart():
    return os.system('sudo systemctl restart zero-exporter')

def exporterState():
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1','/org/freedesktop/systemd1')
    manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    exporter_unit = manager.LoadUnit('zero-exporter.service')
    exporter_proxy = bus.get_object('org.freedesktop.systemd1', str(exporter_unit))
    exporter_properties = Interface(exporter_proxy, dbus_interface='org.freedesktop.DBus.Properties')
    return exporter_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
