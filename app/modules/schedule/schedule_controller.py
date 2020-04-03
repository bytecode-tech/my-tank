from flask import (Blueprint, request)
from .schedule import Scheduler
from .schedule import UserJob

schedule_controller = Blueprint('schedule-controller', __name__, url_prefix='/api/schedule')

def job_response(job):
    return {
        'id': job.id,
        'schedule': job.schedule,
        'command': job.command,
        'device' : job.device,
        'child_plug' : job.child_plug,
        'action' : job.action,
        'comment' : job.comment,
        'enabled' : job.enabled
    }

@schedule_controller.route('/jobs', methods=["GET"])
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
    scheduler = Scheduler()

    if request.method == "GET":
        user_job = scheduler.find_job(id)

    if request.method == "POST":
        user_job = UserJob(id, request.data.get('schedule'), request.data.get('device'), request.data.get('child_plug'), request.data.get('action'), request.data.get('comment'), request.data.get('enabled'))
        user_job = scheduler.save_job(user_job)

    if request.method == "DELETE":
        user_job = scheduler.delete_job(id)
    
    if user_job:
        return job_response(user_job)
    else:
        return {
            'id': "",
            'schedule': "",
            'action' : "",
            'device' : "",
            'child_plug': "",
            'command': "",
            'comment' : "",
            'enabled' : ""
        }
    
