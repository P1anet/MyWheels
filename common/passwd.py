import os
import sys
import getpass
import base64
from common.constant import *
from common.utils import *


def change_string_to_base64_string(code):
    return base64.encodebytes(bytes(code.encode('utf-8'))).decode('utf-8')


def change_base64_string_to_string(code):
    return base64.b64decode(code).decode('utf-8')


def encrypt_cipher(code):
    result = change_string_to_base64_string(code)
    print(result)
    # result = change_string_to_base64_string(result)
    with open('{}/.env'.format(COMMON_DIR), 'w', encoding='utf-8') as f:
        f.write(result)


def decrypt_cipher():
    with open('{}/.env'.format(COMMON_DIR), 'r', encoding='utf-8') as f:
        res = f.read()
        if res:
            result = res.split('\n')[0]
            code = change_base64_string_to_string(result)
            # code = change_base64_string_to_string(code)
            return code
        else:
            return None


def save_cipher():
    for i in range(3):
        passwd = getpass.getpass('Please enter your password!')
        passwd_ed = getpass.getpass('Please enter your password again!')
        if passwd_ed == passwd:
            cmd = 'echo {}| sudo -S ls /root > /dev/null'.format(passwd)
            res = shell_execute(cmd, False)
            if res[0]:
                print('password is not correct, please enter your password again')
                continue
            else:
                encrypt_cipher(passwd)
                return passwd
        else:
            print('two passwords are not equal, please enter your password again')
            continue
    
    return None


def check_passwd_exist():
    if not os.path.exists('{}/.env'.format(COMMON_DIR)):
        return False
    code = decrypt_cipher()
    if not code:
        return False
    if code:
        cmd = 'echo {}| sudo -S ls /root > /dev/null'.format(code)
        res = shell_execute(cmd, False)
        return not res[0]


def retype_passwd():
    if check_passwd_exist():
        passwd = decrypt_cipher()
        cmd = 'echo {}| sudo -S ls /root > /dev/null'.format(passwd)
        res = shell_execute(cmd, False)
        if res[0]:
            print('passwd in env is wrong, deleting...')
            cmd = 'rm -f {}/.env'.format(COMMON_DIR)
            shell_execute(cmd)
        else:
            return passwd
    passwd = save_cipher()
    if passwd:
        return passwd
    else:
        print('entering password failed in 3 times, exiting...')
        sys.exit(-1)


if __name__ == '__main__':
    encrypt_cipher('hello')
    res = decrypt_cipher()
    print(res)