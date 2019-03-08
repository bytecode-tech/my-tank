#!/usr/bin/python
import git
import os
from dbus import SystemBus, Interface
import docker

def update_source():
    g = git.Git('/home/pi/zero-appliance')
    return g.pull('origin')

def check_update():
    g = git.Git('/home/pi/zero-appliance')
    g.fetch('origin')
    return g.status('-uno')

def appliance_restart():
    return os.system('sudo systemctl restart zero-appliance')

def appliance_state():
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1','/org/freedesktop/systemd1')
    manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    appliance_unit = manager.LoadUnit('zero-appliance.service')
    appliance_proxy = bus.get_object('org.freedesktop.systemd1', str(appliance_unit))
    appliance_properties = Interface(appliance_proxy, dbus_interface='org.freedesktop.DBus.Properties')
    return appliance_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')

def app_state():
    client = docker.from_env()
    container = client.containers.get('weegrow_app')
    return container.status
