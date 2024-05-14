import os
import hashlib

STORE_DIR = 'store'

def get_file_path(file_hash):
    subdir = file_hash[:2]
    return os.path.join(STORE_DIR, subdir, file_hash)

def save_file(file_data):
    file_hash = hashlib.sha256(file_data).hexdigest()
    file_path = get_file_path(file_hash)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(file_data)
    return file_hash

def delete_file(file_hash):
    file_path = get_file_path(file_hash)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def get_file(file_hash):
    file_path = get_file_path(file_hash)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    return None
