from init.init import *
from cli.client import *
from secure.secure import *
import os
from collections import namedtuple


def start_terminal():
    disk_path = os.path.join(os.path.dirname(__file__),  "Disk:L")
    init_data = decode("E:\PycharmProjects\SPBD_labs\lab1\data.json")
    init_disk(disk_path, init_data)
    user_password = password()
    flag = True
    while flag:
        try:
            user = users[user_password]
            print('You login as {}'.format(user))
            flag = False
        except KeyError:
            print('Incorrect password')
            user_password = password()

    disk = decode(disk_path)
    nt = namedtuple('state', ['user', 'current_dir', 'disk', 'file', 'content'])
    state = nt(user, '/', disk, False, content='')
    cli_line(state)

if __name__ == "__main__":
    start_terminal()

