#!/usr/bin/python
import git
import dbus

def updateSource():
    g = git.Git('/home/pi/zero-appliance')
    return g.pull('origin')

def checkUpdate():
    g = git.Git('/home/pi/zero-appliance')
    return g.status()

def restartAppliance():
    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
    return manager.RestartUnit('zero-appliance.service', 'fail')