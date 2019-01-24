from flask import (Blueprint, request)
from .schedule import Scheduler
from .schedule import UserJob

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

def job_response(job):
    return {
        'id': job.id,
        'schedule': job.schedule,
        'command': job.command,
        'comment' : job.comment,
        'enabled' : job.enabled
    }

@schedule_controller.route('/', methods=["GET"])
def api_schedule_control():
    scheduler = Scheduler()
    job_list = scheduler.jobs()
    response_list = []
    for job in job_list:
        response_list.append(job_response(job))

    return {'schedule': response_list}

@schedule_controller.route('/jobs/<id>', methods=["GET", "POST", "DELETE"])
def api_job_control(id):
    user_job = None

    if request.method == "GET":
        scheduler = Scheduler()
        user_job = scheduler.find_job(id)

    if request.method == "POST":
        user_job = UserJob(id, request.data.get('schedule'), request.data.get('command'), request.data.get('comment'))
        scheduler = Scheduler()
        user_job = scheduler.save_job(user_job)
    
    return job_response(user_job)
