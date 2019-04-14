#!/usr/bin/python
import functools
import threading
import re
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
        self.id = None
        self.schedule = None
        self.agent = None
        self.action = None
        self.command = None
        self.comment = None

        if 'cron_job' in kwargs:
            cron_job = kwargs.get('cron_job')
            self.schedule = cron_job.slices.render()
            self.command = cron_job.command

            command_components = cron_job.command.rsplit("/")
            component_count = len(command_components)
            if component_count >= 2:
                self.agent = command_components[-2].lower()
                self.action = command_components[-1].lower()            
            
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
            self.agent = args[2].lower()

            # handle booleans
            if isinstance(args[3], bool):
                if args[3]:
                    self.action = "on"
                else:
                    self.action = "off"
            else:
                self.action = args[3].lower()

            self.comment = args[4]
            self.enabled = args[5]

class Scheduler(metaclass=Singleton):
    def jobs(self):
        jobList = []
        cron = CronTab(user=True)
        for job in cron:
            jobList.append(UserJob(cron_job=job))

        return jobList

    def save_job(self, user_job):
        cron = CronTab(user=True)
        job = self.__find_cron_job(cron, user_job.id)

        if job:
            job.setall(user_job.schedule)
            job.set_command("curl -X POST http://localhost:8080/api/" + user_job.agent + "/" + user_job.action)
            job.set_comment(user_job.id + ';' + user_job.comment)
            job.enable(user_job.enabled)
        else:
            job = cron.new(command="curl -X POST http://localhost:8080/api/" + user_job.agent + "/" + user_job.action)
            job.setall(user_job.schedule)
            job.set_comment(user_job.id + ';' + user_job.comment)

        cron.write()

        saved_job = self.__find_cron_job(cron, user_job.id)

        if saved_job:
            return UserJob(cron_job=saved_job)
        else:
            return None
    
    def __find_cron_job(self, cron_tab, job_id):
        jobs = cron_tab.find_comment(re.compile(r"^" + re.escape(job_id)))

        return next(jobs, None)

    def find_job(self, job_id):
        cron = CronTab(user=True)
        job = self.__find_cron_job(cron, job_id)

        if job:
            return UserJob(cron_job=job)
        else:
            return None
        

    def delete_job(self, job_id):
        cron = CronTab(user=True)
        job = self.__find_cron_job(cron, job_id)

        if job:
            cron.remove(job)
            cron.write()

        return None

        
