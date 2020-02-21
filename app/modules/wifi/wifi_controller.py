from flask import (Blueprint, request, jsonify)
from . import Network, WifiNetwork, Wifi
import os

wifi_controller = Blueprint('wifi-controller', __name__, url_prefix='/api/wifi')


def wifi_network_response(wifi_network):
    return {
        'bssid': wifi_network.bssid,
        'ssid': wifi_network.ssid,
        'channel': wifi_network.channel,
        'frequency': wifi_network.frequency,
        'mode': wifi_network.mode,
        'type': wifi_network.type,
        'privacy': wifi_network.privacy,
        'signal_dbm': wifi_network.signal_dbm,
        'signal_quality': wifi_network.signal_quality
    }

def network_response(network):
    if network:
        return {
            'enabled': network.enabled,
            'ssid':  network.ssid,
            'priority': network.priority,
            'path': network.path
        }
    else:
        return {
            'enabled': '',
            'ssid':  '',
            'priority': '',
            'path': ''
        }
    return {
        'enabled': network.enabled,
        'ssid':  network.ssid,
        'priority': network.priority,
        'path': network.path
    }

@wifi_controller.route('/server/wifi/scan', methods=["GET"])
def api_wifi_ssids():
    if request.method == "GET":
        
        networks = Wifi().scan()

        response_list = []
        for wifi_network in networks:
            response_list.append(wifi_network_response(wifi_network))

        return {'wifiNetworksAvailable': response_list}

@wifi_controller.route('/server/wifi/networks', methods=["GET", "POST"])
def api_wifi_networks():
    wifi = Wifi()
    if request.method == "POST":
        wifi.save_config()

    saved_networks = wifi.get_known_networks()

    response_list = []
    for saved_network in saved_networks:
        response_list.append(network_response(saved_network))

    return {'savedNetworks': response_list}

@wifi_controller.route('/server/wifi/networks/<name>', methods=["GET", "POST", "DELETE"])
def api_wifi_network(name):
    wifi = Wifi()
    if request.method == "GET":
        return {'network': network_response(wifi.get_network_info(name))}
    elif request.method == "POST":
        psk = request.data.get('psk')
        enabled = request.data.get('enabled', 'True') == 'True'
        priority = request.data.get('priority', '0')
        saved_network = wifi.save_network(name, psk, enabled, priority)

        return {'network': network_response(saved_network)}
    elif request.method == "DELETE":
        wifi.delete_network(name)
        return {'network': network_response(wifi.get_network_info(name))}

@wifi_controller.route('/server/wifi/networks/active', methods=["GET"])
def api_active_networks():
    if request.method == "GET":
        active_network = Wifi().get_active_network()

        return {'networks': network_response(active_network)}

@wifi_controller.route('/server/wifi/networks/<name>/activate', methods=["GET", "POST"])
def api_activate_network(name):
    wifi = Wifi()
    if request.method == "GET":
        active_name = wifi.get_active_network().ssid
        if name.lower() == active_name.lower():
            return{'isActive': "True"}
        else:
            return {'isActive': "False"}
    elif request.method == "POST":
        wifi.activate_network(name)

        return{'isActive': "True"}

@wifi_controller.route('/server/wifi/networks/ap-mode', methods=["GET", "POST", "DELETE"])
def api_network_ap_mode():
    wifi = Wifi()
    if request.method == "POST":
        wifi.enable_ap_mode()
    elif request.method == "DELETE":
        wifi.disable_ap_mode()

    if wifi.is_ap_mode:
        return{'isApMode': "True"}
    else:
        return {'isApMode': "False"}
