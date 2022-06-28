from cmds.commands import *
from cmds.helpers import *
from secure.operations import *
import json
import os, time


def cli_line(state, start_time):
    answer = input('') if state.file else input(str(state.current_dir) + ':$ ')
    command = ''
    params = ''
    [command, *params] = answer.split(' ')
    if (command not in commands) and (state.file == False):
        print('Incorrect command "' + command + '"')
        command_error = errors['incorrect_command']
        command_error(state.user, command)
    elif state.file:
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
    if start_time - time.time() <= -30:
        att = question_for_user(state)

        start_time = time.time()
    cli_line(state, start_time)


def question_for_user(state, count=0):
    disk_path = os.path.join(os.path.dirname(__file__) , ".." , "Disk:L")
    init_data = state.disk
    init_disk(disk_path , init_data)
    disk = decode(disk_path)

    all_users = disk['files']['secure']['files']['register']['content']
    all_users = json.loads(all_users)

    for i in all_users:
        if i['login'] == state.user and i['login'] != 'admin':
            number_question = i['question']
            data_questions = decode("E:/PycharmProjects/SPBD_labs/lab2/questions.json")
            print(data_questions['questions'][number_question])
            answer = input("Your answer: ")
            if answer == i['answer']:
                return True
            else:
                command_error = errors['incorrect_answer']
                command_error(state.user)
                if count > 1:
                    print("You need to re-register !")
                    os._exit(0)
                count += 1
                return question_for_user(state, count)





