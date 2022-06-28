from secure.secure import *
import time


def incorrect_command(user, command):
    operation('Incorrect command {}'.format(command), 3, user)


def incorrect_params_length(user):
    operation('Incorrect params length', 3, user)


def unknown_path(user):
    operation('Unknown path', 3, user)


def permission_denied(user):
    operation('Permission denied', 3, user)


def not_dir(user):
    operation('This is not a directory!', 3, user)


def incorrect_answer(user):
    operation('Incorrect answer', 3, user)


def unknown_user(user):
    operation('Unknown user', 3, user)


def login_time_passed(user):
    operation('Login time is passed', 3, user)


def excess_number_of_users(user):
    operation('Excess number of new users', 3, user)


def password_not_same(user):
    operation('Password and repeated password not same', 3, user)


def password_short(user):
    operation('Password is too short', 3, user)


def exceeded_limit(user):
    operation('You have exceeded the login limit', 3, user)


def not_file(user):
    operation('This is not a file!', 3, user)


def incorrect_login_or_password(user):
    operation('Incorrect login or password', 3, user)


def expired_password(user):
    operation('This user\'s password has expired. Contact the administrator for help', 3, user)


errors = {'incorrect_command': incorrect_command, 'incorrect_params_length': incorrect_params_length, 'unknown_path':
    unknown_path, 'permission_denied': permission_denied, 'not_dir': not_dir, 'incorrect_answer': incorrect_answer,
          'unknown_user': unknown_user, 'login_time_passed': login_time_passed, 'excess_number_of_users':
              excess_number_of_users, 'password_not_same': password_not_same, 'password_short': password_short,
          'exceeded_limit': exceeded_limit, 'not_file': not_file, 'incorrect_login_or_password':
              incorrect_login_or_password, 'expired_password': expired_password}


def operation(message, lvl, user):
    operation_log = decode("E:/PycharmProjects/SPBD_labs/lab3/errs.json")
    operation_log['operations'][user].append({'operation': {'date': time.ctime(), 'user': user, 'level': lvl,'message': message}})
    encode("E:/PycharmProjects/SPBD_labs/lab3/errs.json", operation_log)