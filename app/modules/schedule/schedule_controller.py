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
        schedule = request.data.get('schedule')
        command = request.data.get('command')
        comment = request.data.get('comment')
        user_job = UserJob(schedule, command, comment)
        scheduler = Scheduler()
        schedule.save_job(user_job)
    
    return {'schedule': schedule,
            'command': command,
            'comment': comment}
