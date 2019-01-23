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
            self.comment = cron_job.comment
            self.enabled = cron_job.is_enabled()
        else:
            self.schedule = args[0]
            self.command = args[1]
            self.comment = args[2]

class Scheduler():
    __metaclass__ = Singleton

    def jobs(self):
        cron = CronTab(user=True)
        return cron

    def save_job(self, user_job):
        cron = CronTab(user=True)
        job = cron.new(command=user_job.command, user='root')
        job.setall(user_job.schedule)
        job.set_comment(user_job.comment)
        cron.write()
        return UserJob(cron_job=job)

    def serializable_jobs(self):
        jobList = []
        cron = CronTab(user=True)
        for job in cron:
            jobList.append(UserJob(cron_job=job))

        return jobList
        
