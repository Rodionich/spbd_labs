from cli.client import *
from cli.rl import *
import sys, os
import time
from threading import *
import json


def verify_user(all_users, user_data):

    selected_user = None
    for i in all_users:
        if user_data['login'] == dict(i)['login'] and user_data['password'] == dict(i)['password']:
            selected_user = i
    return selected_user


login_time = 60*5
login_attempts = 3
users_length = 6
time_valid = 60*60*24*2
admin_password_length = 3
user_password_length = 3


def verify_user_with_rules(disk, attempts=login_attempts, time_wait=login_time):

    done = False

    def wait_func():
        if not done:
            print('\nLogin time is passed')
            os._exit(0)

    timer_id = Timer(60, wait_func)
    timer_id.start()

    all_users = disk['files']['secure']['files']['register']['content']
    all_users = json.loads(all_users)

    for i in range(attempts):
        user_data = cli_questions([{'name': 'login', 'question': 'User login: ', 'secure' : False}, {'name': 'password', 'question':'Password:', 'secure': True}])
        selected_user = verify_user(all_users, user_data)
        if not selected_user:
            print("Incorrect login or password")
            continue
        elif selected_user.get('time', False) and time.time() - selected_user.get('time', False) > time_valid:
            print("This user\'s password has expired. Contact the administrator for help")
            continue
        else:
            done = True
            if selected_user.get('time', False):
                print('Your password is valid until ' + str(time.ctime(selected_user.get('time', False) + time_valid)))
            return user_data

    done = True
    timer_id.cancel()
    print("You have exceeded the login limit")
    os._exit(0)












