from flask import (Blueprint, request)
from .schedule import Scheduler

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

def job_response(job):
    return {
        'schedule': job.schedule,
        'command': job.command,
        'comment' : job.comment,
        'enabled' : job.enabled
    }

@schedule_controller.route('/', methods=["GET"])
def api_schedule_control():
    scheduler = Scheduler()
    jobList = scheduler.serializableJobs()
    responseList = []
    for job in jobList:
        responseList.append(job_response(job))

    return {'schedule': responseList}
