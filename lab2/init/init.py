import os
from secure.secure import *


def init_disk(file_path, init_data):
    if os.path.exists(file_path):
        return
    else:
        encode(file_path, init_data)




