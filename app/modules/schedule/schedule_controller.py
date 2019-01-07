from flask import (Blueprint, request)
from crontab import CronTab
from .schedule import ScheduledJob

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

@schedule_controller.route('/', methods=["GET"])
def api_schedule_control():
    system_cron = CronTab(tabfile='/etc/crontab', user=False)
    jobList = []
    for job in system_cron:
        jobList.append(ScheduledJob(job))

    return {'schedule': jobList}
