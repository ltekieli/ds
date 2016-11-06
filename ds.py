#!/usr/bin/python

import json
import os
import random
import string
import urllib2

from decimal import Decimal
from api import AuthApi, TaskApi

class Session:
    def __init__(self, host, port, username, password):
        self.auth_api = AuthApi(host, port)
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __enter__(self):
        self.id = self.auth_api.login(self.username, self.password)
        self.task_api = TaskApi(self.host, self.port, self.id)
        return self

    def __exit__(self, type, value, traceback):
        self.auth_api.logout()


def print_tasks(tasks):
    TASK_NAME_LENGTH = 50
    for task in tasks:
        if (len(task['title']) < TASK_NAME_LENGTH):
            task_name = task['title'][0:TASK_NAME_LENGTH]
        else:
            task_name = task['title'][0:TASK_NAME_LENGTH] + "..."
        task_length = len(task_name)
        if (task_length < TASK_NAME_LENGTH):
            task_name += ' ' * (TASK_NAME_LENGTH - task_length)
        try:
            progress = Decimal(task['additional']['transfer']['size_downloaded']) / Decimal(task['size']) * 100
            print "%s\t%s\t%0.2fMB/s\t%0.1f%%" % (task_name, task['status'], Decimal(task['additional']['transfer']['speed_download']) / 1000 / 1000, progress)
        except:
            pass


def main():
    with Session("192.168.1.250", 5000, os.environ['SYNO_USER'], os.environ['SYNO_PASSWD']) as session:
        data = session.task_api.list().data
        # print json.dumps(data, indent=2)
        print_tasks(data["tasks"])

if __name__ == "__main__":
    main()