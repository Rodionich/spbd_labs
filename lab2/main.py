from init.init import *
from cli.client import *
from secure.secure import *
from secure.access import *
import os
from collections import namedtuple


def start_terminal():
    disk_path = os.path.join(os.path.dirname(__file__), "Disk:L")
    init_data = decode("E:/PycharmProjects/SPBD_labs/lab2/journal.json")
    init_disk(disk_path, init_data)
    disk = decode(disk_path)
    user_data = verify_user_with_rules(disk)
    nt = namedtuple('state', ['user', 'current_dir', 'disk', 'file', 'content'])
    state = nt(user_data['login'], '/', disk, False, content='')
    start_time = time.time()
    cli_line(state, start_time)


if __name__ == "__main__":
    start_terminal()

