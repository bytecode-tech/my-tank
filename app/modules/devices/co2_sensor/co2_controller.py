from flask import (Blueprint, request)
from . import co2

temp_controller = Blueprint('temp-controller', __name__, url_prefix='/api/co2')

@temp_controller.route('/', methods=["GET"])
def api_temp_control():

    return co2.read()