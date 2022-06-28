import json


def encode(file_path, content):
    with open(file_path, "w") as write_file:
        encoded_data = json.dumps(content, indent=4)
        write_file.write(encoded_data)
    write_file.close()


def decode(file_path):
    with open(file_path, 'r') as f:
        decoded_data = json.load(f)
    return decoded_data