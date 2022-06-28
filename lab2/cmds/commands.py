from secure.secure import *
from secure.access import *
from cmds.helpers import *
from cli.rl import *
from init.init import *
import time
import sys, os
import json
import threading


def exit_command(newState, params):
    print('Goodbye!')
    time.sleep(0.5)
    sys.exit()


def ls_command(newState, params):
    if len(params) != 0:
        print('Incorrect params length')
        return
    dir_obj = get_dir_obj(newState.disk, newState.current_dir)
    if newState.user not in dir_obj['rights']['read']:
        print('Permission denied')
        return
    for file_name in dir_obj['files']:
        if dir_obj['files'][file_name]['type'] == 'directory':
            print('\033[33m{}\033[0m'.format(file_name))
        else:
            print(file_name)
    return newState


def cd_command(newState, params):
    if len(params) != 1:
        print("Incorrect params length")
        return
    if params[0] == '..':
        file_names = filter(None, (newState.current_dir).split('/'))
        file_names = list(file_names)
        file_names.pop()
        new_dir = '/' + '/'.join(file_names) + '/'
        newState = newState._replace(current_dir= new_dir)
        return newState
    dir_obj = get_dir_obj(newState.disk, newState.current_dir, params[0])
    if not dir_obj:
        return
    if dir_obj['type'] != 'directory':
        print("This is not a directory!")
        return
    if newState.user not in dir_obj['rights']['read']:
        print('Permission denied')
        return
    previous_dir = newState.current_dir
    newState = newState._replace(current_dir=previous_dir + str(params[0]) + '/')
    return newState


def mkdir_command(newState, params):
    if len(params) != 1:
        print('Incorrect params length')
        return
    dir_obj = get_dir_obj(newState.disk, newState.current_dir)
    if not dir_obj:
        print('Unknown path')
        return
    if newState.user not in dir_obj['rights']['write']:
        print('Permission denied')
        return
    newState = newState._replace(disk = create_disk(newState.disk, newState.current_dir, params[0], newState.user))
    disk_path = os.path.join(os.path.dirname(__file__), "..", "Disk:L")
    encode(disk_path, newState.disk)


def rm_command(newState, params):
    if len(params) != 1:
        print('Incorrect params length')
        return
    dir_obj = get_dir_obj(newState.disk, newState.current_dir, params[0])
    if not dir_obj:
        print('Unknown path')
        return
    if newState.user not in dir_obj['rights']['delete']:
        print('Permission denied')
        return
    newState = newState._replace(disk=delete_disk(newState.disk , newState.current_dir, params[0]))
    disk_path = os.path.join(os.path.dirname(__file__),  ".." , "Disk:L")
    encode(disk_path, newState.disk)


def vi_command(newState, params):
    if len(params) != 1:
        print('Incorrect params length')
        return
    dir_obj = get_dir_obj(newState.disk, newState.current_dir, params[0])
    if not dir_obj:
        newState = newState._replace(disk=create_disk(newState.disk, newState.current_dir , params[0] , newState.user))
        disk_path = os.path.join(os.path.dirname(__file__), "..", "Disk:L")
        encode(disk_path , newState.disk)
    else:
        if newState.user not in dir_obj['rights']['write']:
            print('Permission denied')
            return
        if newState.user not in dir_obj['rights']['read']:
            print('Permission denied')
            return
        if dir_obj['type'] != 'file':
            print("This is not a file!")
            return
    newfile = params[0]
    if newfile == 'register':
        newcontent = json.loads(dir_obj['content'])
        print("\nЖурнал реєстрації користувачів\n")
        print("Login  | Password |   Time   | Question | Answer |")
        for i in newcontent:
            if len(i.keys()) > 2:
                print('{}      {}     {}     {}        {}'.format(i['login'], i['password'], int(i['time']),
                                                                  i['question'], i['answer']))
            else:
                print('{}      {}'.format(i['login'], i['password']))
    else:
        newcontent = dir_obj['content']
        newState = newState._replace(file=newfile, content=newcontent)
        print(newState.content)


def pwd_command(newState, params):
    if len(params) != 0:
        print('Incorrect params length')
        return
    print(newState.current_dir)


def whoami_command(newState, params):
    if len(params) != 0:
        print("Incorrect params length")
        return
    print(newState.user)


def su_command(newState, params):
    if len(params) != 0:
        print("Incorrect params length")
        return
    user_data = verify_user_with_rules(newState.disk)
    new_user = user_data['login']
    new_current_dir = '/'
    newState = newState._replace(current_dir = new_current_dir, user = new_user)
    return newState


def new_user(old_users, new_user_inf):
    find = False
    new_user_obj = {'login' : new_user_inf['login'], 'password' : new_user_inf['password'], 'time' : time.time() }

    def new_users(old_users):
        for user in old_users:
            if user['login'] == new_user_inf['login']:
                find = True
                return new_user_obj
            return user

    new_users = new_users(old_users)
    if find:
        return new_users
    return new_user_obj


def cuser_command(newState, params):
    if newState.user != 'admin':
        print("Permission denied")
        return
    if len(params) != 0:
        print("Incorrect params length")
        return

    done = False

    def wait_func():
        if not done:
            print("\nLogin time is passed")
            os._exit(0)

    timer_id3 = threading.Timer(30, wait_func)
    timer_id3.start()

    disk_path = os.path.join(os.path.dirname(__file__) , "..",  "Disk:L")
    init_data = newState.disk
    init_disk(disk_path , init_data)
    disk = decode(disk_path)

    all_users = disk['files']['secure']['files']['register']['content']
    all_users = json.loads(all_users)
    if len(all_users) >= users_length:
        print("Excess number of new users")
        return

    for i in range(login_attempts):
        new_user_inf = cli_questions([{'name': 'login', 'question': 'New user login: ', 'secure': False},
                                      {'name': 'password', 'question':'', 'secure': True}, {'name': 'repeatPassword', 'secure': True, 'question': 'Repeat password: '}])
        if new_user_inf['password'] != new_user_inf['repeatPassword']:
            print("Password and repeated password not same")
            continue
        if new_user_inf['login'] == 'admin' and len(new_user_inf['password']) < admin_password_length:
            print("Password is too short")
            continue
        if new_user_inf['login'] != 'admin' and len(new_user_inf['password']) < user_password_length:
            print("Password is too short")
            continue

        done = True
        new_users = new_user(all_users, new_user_inf)

        secret_question_info = add_question()
        new_users.update(secret_question_info)

        newState = newState._replace(disk=add_new_user(newState.disk, new_users))
        disk_path = os.path.join(os.path.dirname(__file__), "..", "Disk:L")
        encode(disk_path, newState.disk)

        break

    return newState

    timer_id3.cancel()
    done = True
    print("You have exceeded the login limit")
    os._exit(0)


commands = {'exit': exit_command, 'ls': ls_command, 'cd': cd_command, 'mkdir': mkdir_command, 'rm': rm_command,
            'vi': vi_command, 'pwd': pwd_command, 'su': su_command, 'cuser': cuser_command, 'whoami' : whoami_command}



