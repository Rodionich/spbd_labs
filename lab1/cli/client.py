from cmds.commands import *
from cmds.helpers import *
import getpass
import json
import os

def password():
    return getpass.getpass()


def cli_line(state):
    answer = input('') if state.file else input(str(state.current_dir) + ':$ ')
    command = ''
    params = ''
    [command, *params] = answer.split(' ')
    if (command not in commands) and (state.file == False):
        print('Incorrect command "' + command + '"')
    elif state.file:
        print(state.file)
        state.disk = json.load(json.dumps(create_disk(state.disk, state.currentDir, params[0], state.user, 'file')))
        disk_path = os.path.join(os.path.dirname(__file__), "..", "..", "Disk:L")
        encode(disk_path, state.disk)
        state.remove(state.file)
        state.remove(state.content)
    else:
        command_func = commands[command]
        temp = command_func(state, params)
        if temp:
            state = temp
    cli_line(state)

