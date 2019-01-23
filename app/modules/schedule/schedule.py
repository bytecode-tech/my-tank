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
    

class Scheduler():
    __metaclass__ = Singleton
    
    def __init__(self):
        self.system_cron = CronTab(tabfile='/etc/crontab', user=False)

    def jobs(self):
        return self.system_cron

    def serializableJobs(self):
        jobList = []
        for job in self.system_cron:
            jobList.append(UserJob(cron_job=job))

        return jobList
        
