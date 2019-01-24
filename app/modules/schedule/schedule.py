#!/usr/bin/python
import functools
import threading
from crontab import CronTab

lock = threading.Lock()

def synchronized(lock):
    """ Synchronization decorator """
    def wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kw):
            with lock:
                return f(*args, **kw)
        return inner_wrapper
    return wrapper


class Singleton(type):
    _instances = {}

    @synchronized(lock)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class UserJob():
    def __init__(self, *args, **kwargs):
        if 'cron_job' in kwargs:
            cron_job = kwargs.get('cron_job')
            self.schedule = cron_job.slices.render()
            self.command = cron_job.command
            
            comment_data = cron_job.comment.split(';')
            stringcount = len(comment_data)

            if stringcount == 2:
                self.id = comment_data[0]
                self.comment = comment_data[1]
            else:
                self.id = None
                self.comment = cron_job.comment

            self.enabled = cron_job.is_enabled()
        else:
            self.id = args[0]
            self.schedule = args[1]
            self.command = args[2]
            self.comment = args[3]

class Scheduler():
    __metaclass__ = Singleton

    def jobs(self):
        jobList = []
        cron = CronTab(user=True)
        for job in cron:
            jobList.append(UserJob(cron_job=job))

        return jobList

    def save_job(self, user_job):
        cron = CronTab(user=True)
        job = cron.new(command=user_job.command, user='root')
        job.setall(user_job.schedule)
        job.set_comment(user_job.id + ';' + user_job.comment)
        cron.write()
        return UserJob(cron_job=job)
    
    def find_job(self, job_id):
        cron = CronTab(user=True)
        jobs = cron.find_comment(job_id)

        job = next(jobs, None)

        if job:
            return UserJob(cron_job=job)
        else:
            return None
        

    def delete_job(self, job_id):
        cron = CronTab(user=True)
        jobs = cron.find_comment(job_id)

        job = next(jobs, None)

        if job:
            cron.remove(job)

        return self.find_job(job_id)

        
