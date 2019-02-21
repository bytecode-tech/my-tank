#!/usr/bin/python
import git

def updateSource():
    g = git.Git('/home/pi/zero-appliance')
    return g.pull('origin')

def checkUpdate():
    g = git.Git('/home/pi/zero-appliance')
    return g.status()
