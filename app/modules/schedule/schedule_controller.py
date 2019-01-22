from flask import (Blueprint, request)
from .schedule import Scheduler

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

def job_repr(job):
    return {
        'schedule': job.slices.render(),
        'command': job.command,
        'comment' : job.comment,
        'enabled' : job.is_enabled()
    }

@schedule_controller.route('/', methods=["GET"])
def api_schedule_control():
    scheduler = Scheduler()
    cronList = scheduler.jobs()
    jobList = []
    for job in cronList:
        jobList.append(job_repr(job))

    return {'schedule': jobList}
