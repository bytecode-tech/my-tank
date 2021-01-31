from flask import (Blueprint, request)
from . import co2

co2_controller = Blueprint('co2-controller', __name__, url_prefix='/api/co2')

@co2_controller.route('/', methods=["GET"])
def api_co2_control():

    return co2.read()