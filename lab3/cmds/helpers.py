import json
from secure.secure import *


def get_dir_obj(disk, current_dir, file=''):
    obj = disk
    names = filter(None, (current_dir + file).split('/'))
    for name in names:
        try:
            obj = obj['files'][name]
        except Exception:
            print('Unknown path')
            return
    return obj


def delete_loop(disk, keys, count=0):

    def remove(dir_files , length , reverse_keys):
        if length == 0:
            return dir_files
        else:
            return remove(dir_files.copy()[reverse_keys[length]]['files'], length - 1, reverse_keys)


    if (len(keys)-1) == count:
        del disk['files'][keys[count]]
        return disk
    else:
        disk_paste = 0
        dir_files = disk.copy()['files']
        disk_remove = remove(dir_files, len(keys)-1, keys[::-1])
        del disk_remove[keys[-1]]
        return disk


def delete_disk(disk, current_dir, file=''):
    file_names = list(filter(None, (current_dir + file).split('/')))
    return delete_loop(disk, file_names, 0)


def create_loop(disk, keys, count=0, user = 'admin', typeof = 'directory'):

    def paste(dir_files, length, reverse_keys):
        if length == 0:
            return dir_files
        else:
            return paste(dir_files.copy()[reverse_keys[length]]['files'], length-1, reverse_keys)

    if (len(keys) - 1) == count:
        (disk['files']).update({keys[count]: {"type": typeof, "rights": {"read": user, "write": user, "delete": user}, "files": {} }})
        return disk
    else:
        disk_paste = 0
        dir_files = disk.copy()['files']
        disk_paste = paste(dir_files, len(keys)-1, keys[::-1])
        disk_paste.update({keys[len(keys)-1]: {"type": typeof , "rights": {"read": user , "write": user , "delete": user} , "files": {}}})
        return disk


def create_disk(disk, current_dir, file = '', user = 'admin', typeof = 'directory'):
    file_names = list(filter(None, (current_dir + file).split('/')))
    return create_loop(disk, file_names, 0, user, typeof)


def add_new_user(disk, new_user):
    operation_log = decode("E:/PycharmProjects/SPBD_labs/lab3/errs.json")
    internal_dict = {new_user['login']: []}
    operation_log['operations'].update(internal_dict)
    encode("E:/PycharmProjects/SPBD_labs/lab3/errs.json", operation_log)

    disk1 = disk
    for i in disk1['rights'].values():
        i.append(new_user['login'])

    disk_copy = disk1.copy()['files']['secure']['files']['register']['content']
    disk_copy = json.loads(disk_copy)
    disk_copy.append(new_user)

    disk1['files']['secure']['files']['register'] = {"type": "file", "rights": {"read": ["admin"], "write": ["admin"], "delete": ["admin"]}, 'content': (str(disk_copy)).replace('\'', '\"')}
    return disk1


