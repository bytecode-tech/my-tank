#!/usr/bin/python
import git
import os
from dbus import SystemBus, Interface
import docker
import logging
import time

def update_source():
    g = git.Git('/home/pi/zero-appliance')
    return g.pull('origin')

def check_update():
    g = git.Git('/home/pi/zero-appliance')
    g.fetch('origin')
    return g.status('-uno')

def appliance_update_available():
    git_status = check_update()
    index = git_status.find('up-to-date')
    return True if index < 0 else False

def appliance_restart():
    time.sleep(15)
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

def app_restart():
    client = docker.from_env()
    container = client.containers.get('weegrow_app')
    container.restart()
    return container.status

def app_update_available():
    client = docker.from_env()
    container = client.containers.get('weegrow_app')
    current_image = container.image
    current_tag = container.attrs['Config']['Image']

    latest_image = client.images.pull(current_tag)

    if current_image.id != latest_image.id:
        return True
    else:
        return False

def app_update():
    client = docker.from_env()
    container = client.containers.get('weegrow_app')
    current_image = container.image
    current_tag = container.attrs['Config']['Image']

    latest_image = client.images.pull(current_tag)

    if current_image.id != latest_image.id:
        container = client.containers.get('weegrow_app')
        container.stop()
        container.remove()
        new_container = client.containers.run('joshdmoore/aspen-app:dev', name="weegrow_app", detach=True, network_mode="host", restart_policy={"Name": "on-failure", "MaximumRetryCount": 5})
        return new_container.status
    else:
        return 'No Update Available'

def prometheus_state():
    client = docker.from_env()
    container = client.containers.get('weegrow_prometheus')
    return container.status
