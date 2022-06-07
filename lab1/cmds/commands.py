from secure.secure import *
from cmds.helpers import *
import time
import sys, os
import json


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
    disk_path = os.path.join(os.path.dirname(__file__), ".." , ".." ,"Disk:L")
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
    disk_path = os.path.join(os.path.dirname(__file__),  ".." , ".." , "Disk:L")
    encode(disk_path, newState.disk)


def vi_command(newState, params):
    if len(params) != 1:
        print('Incorrect params length')
        return
    dir_obj = get_dir_obj(newState.disk, newState.current_dir, params[0])
    if not dir_obj:
        newState = newState._replace(disk=create_disk(newState.disk , newState.current_dir , params[0] , newState.user))
        disk_path = os.path.join(os.path.dirname(__file__) , ".." , ".." ,  "Disk:L")
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
    newcontent = dir_obj['content']
    newState = newState._replace(file=newfile, content=newcontent)
    print(newState.content)



def pwd_command(newState, params):
    if len(params) != 0:
        print('Incorrect params length')
        return
    print(newState.current_dir)


commands = {'exit': exit_command, 'ls': ls_command, 'cd': cd_command,'mkdir': mkdir_command, 'rm': rm_command, 'vi': vi_command, 'pwd': pwd_command}



