#!/usr/bin/python
import git
import os
from flask import current_app
from dbus import SystemBus, Interface
import docker
import logging
import uwsgi
import re



_LOGGER = logging.getLogger(__name__)

def update_source():
    g = git.Git(current_app.config['PROJECT_ROOT'])
    return g.pull('origin')

def check_update():
    g = git.Git(current_app.config['PROJECT_ROOT'])
    g.fetch('origin')
    return g.status('-uno')

def appliance_update_available():
    git_status = check_update()
    result = re.search("up.to.date", git_status)
    return True if result is None else False

def update_dependencies():
    return os.system('/opt/observer/venv/bin/pip3 install -r ' + current_app.config['PROJECT_ROOT'] + '/requirements.txt')

def appliance_restart():
    uwsgi.reload()

def appliance_state():
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1','/org/freedesktop/systemd1')
    manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    appliance_unit = manager.LoadUnit('observer-appliance.service')
    appliance_proxy = bus.get_object('org.freedesktop.systemd1', str(appliance_unit))
    appliance_properties = Interface(appliance_proxy, dbus_interface='org.freedesktop.DBus.Properties')
    return appliance_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')

def app_state():
    client = docker.from_env()
    container = client.containers.get('observer_web')
    return container.status

def app_restart():
    client = docker.from_env()
    container = client.containers.get('observer_web')
    container.restart()
    return container.status

def app_update_available():
    client = docker.from_env()
    container = client.containers.get('observer_web')
    current_image = container.image
    current_tag = container.attrs['Config']['Image']

    latest_image = client.images.pull(current_tag)

    if current_image.id != latest_image.id:
        return True
    else:
        return False

def app_update():
    client = docker.from_env()
    container = client.containers.get('observer_web')
    current_image = container.image
    current_tag = container.attrs['Config']['Image']
    current_env = container.attrs['Config']['Env']

    latest_image = client.images.pull(current_tag)

    if current_image.id != latest_image.id:
        container = client.containers.get('observer_web')
        container.stop()
        container.remove()
        new_container = client.containers.run(current_tag, name="observer_web", detach=True, network_mode="host", restart_policy={"Name": "always"}, environment=current_env)
        return new_container.status
    else:
        return 'No Update Available'

def prometheus_state():
    client = docker.from_env()
    container = client.containers.get('observer_prometheus')
    return container.status
