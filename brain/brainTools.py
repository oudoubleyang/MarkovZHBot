import os
import base64
from time import time
from brainInfo import self_id, chat_expire_time


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def write_file(content, filename, encrypt=False):
    if encrypt:
        with open(filename, 'wb') as f:
            f.write(base64.b64encode(content.encode('utf-8')))
        return True
    else:
        with open(filename, 'w') as f:
            f.write(content)
        return True


def query_token(token_id=self_id):
    return read_file(f'token_{token_id}', True)


def del_files(path):
    files = []
    for i in os.listdir(path):
        if os.path.isfile(f'{path}/{i}'):
            files.append(f'{path}/{i}')
    for i in files:
        os.remove(i)
        print(f'[INFO] Deleted {i}')


def remove_inactive_chats(path='../data'):
    files = []
    current = time()
    for i in os.listdir(path):
        if os.path.isfile(f'{path}/{i}'):
            files.append(f'{path}/{i}')
    for i in files:
        if current - os.path.getmtime(i) > chat_expire_time:
            os.remove(i)
            print(f'[INFO] Deleted {i}')


"""
def set_proxy(ip='127.0.0.1', port='1080', protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
"""