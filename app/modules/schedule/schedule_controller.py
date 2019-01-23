from flask import (Blueprint, request)
from .schedule import Scheduler
from .schedule import UserJob

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
    job_list = scheduler.serializable_jobs()
    response_list = []
    for job in job_list:
        response_list.append(job_response(job))

    return {'schedule': response_list}

@schedule_controller.route('/job', methods=["GET", "POST"])
def api_job_control():
    schedule = ""
    command = ""
    comment = ""
    if request.method == "POST":
        user_job = UserJob(request.data.get('schedule'), request.data.get('command'), request.data.get('comment'))
        scheduler = Scheduler()
        job = scheduler.save_job(user_job)
        schedule = job.schedule
        command = job.command
        comment = job.comment
    
    return {'schedule': schedule,
            'command': command,
            'comment': comment}
