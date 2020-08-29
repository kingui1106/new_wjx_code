import json
from pathlib import Path
from secrets import token_bytes
import requests
def random_key(length):
    key = token_bytes(nbytes=length)
    key_int = int.from_bytes(key, 'big')
    return key_int

def decrypt(encrypted, key_int):
    decrypted = encrypted ^ key_int
    length = (decrypted.bit_length() + 7) // 8
    decrypted_bytes = int.to_bytes(decrypted, length, 'big')
    return decrypted_bytes.decode()

def encrypt(raw):
    raw_bytes = raw.encode()
    raw_int = int.from_bytes(raw_bytes, 'big')
    key_int = 19961225
    return raw_int ^ key_int, key_int

def encrypt_file(path, key_path=None, *, encoding='utf-8'):
    path = Path(path)
    cwd = path.cwd() / path.name.split('.')[0]
    path_encrypted = cwd / path.name
    if key_path is None:
        key_path = cwd / 'key'
    if not cwd.exists():
        cwd.mkdir()
        path_encrypted.touch()
        key_path.touch()

    with path.open('rt', encoding=encoding) as f1, \
        path_encrypted.open('wt', encoding=encoding) as f2, \
            key_path.open('wt', encoding=encoding) as f3:
        encrypted, key = encrypt(f1.read())
        json.dump(encrypted, f2)
        json.dump(key, f3)
#Python学习群592539176
def decrypt_file(path_encrypted, key_path=None, *, encoding='utf-8'):
    path_encrypted = Path(path_encrypted)
    cwd = path_encrypted.cwd()
    path_decrypted = cwd / 'decrypted'
    if not path_decrypted.exists():
        path_decrypted.mkdir()
        path_decrypted /= path_encrypted.name
        path_decrypted.touch()
    if key_path is None:
        key_path = cwd / 'key'
    with path_encrypted.open('rt', encoding=encoding) as f1, \
        key_path.open('rt', encoding=encoding) as f2, \
        path_decrypted.open('wt', encoding=encoding) as f3:
        decrypted = decrypt(json.load(f1), json.load(f2))
        f3.write(decrypted)

def encrt_my():
    with open('./1.txt', 'rt', encoding='utf-8') as file:
        encrypted, key = encrypt(file.read())
        file.close()
        with open('./2.json', 'wt', encoding='utf-8') as f2 :
            json.dump(encrypted, f2)

'''
url = "http://118.24.52.95/get_all"
response = requests.get(url)
response_list = eval(response.text)
#with open('./proxy_pool.list', 'w+') as file:
ipList = []
for i in response_list:
    ipList.append(i.get('proxy'))
print(ipList[1])
#zlq
keyint = 19961225
with open('./1.txt', 'w+') as file:
    for ip in ipList:
        file.write(ip)
        file.write('\n')
    file.close()
'''
ipList = None
with open('./2.json', 'rt', encoding='utf-8') as file:
    decrypted = decrypt(json.load(file), 19961225)
    ipList = decrypted.strip().split('\n')
    file.close()






