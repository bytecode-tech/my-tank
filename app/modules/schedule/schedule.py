#!/usr/bin/python

class ScheduledJob():
    
    def __init__(self, cron_job):
        self.cron_schedule = cron_job.slices.render()
        self.command = cron_job.command
        self.comment = cron_job.comment
        
