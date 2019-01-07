from flask import (Blueprint, request)
from crontab import CronTab
from .schedule import ScheduledJob

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
    system_cron = CronTab(tabfile='/etc/crontab', user=False)
    jobList = []
    for job in system_cron:
        jobList.append(job_repr(job))

    return {'schedule': jobList}
