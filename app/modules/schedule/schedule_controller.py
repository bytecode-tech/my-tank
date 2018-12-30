from flask import (Blueprint, request)
import schedule

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

@schedule_controller.route('/', methods=["GET"])
def api_schedule_control():
    return {'schedule': schedule.allJobs()}
