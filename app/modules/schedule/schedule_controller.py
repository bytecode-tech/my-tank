from flask import (Blueprint, request)
from .schedule import Scheduler

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

@schedule_controller.route('/', methods=["GET"])
def api_schedule_control():
    scheduler = Scheduler()

    return {'schedule': scheduler.serializableJobs()}
