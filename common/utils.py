import os
import sys
import csv
import json
import yaml
import pickle
import subprocess
import getpass
import argparse
from datetime import datetime
from typing import *
from statistics import mean
from common.constant import *

# -----Time-----
def get_timestamp():
    return time.strftime(TIME_PATTERN["timestamp"], time.localtime(time.time()))

def utctime_to_beijing_timestamp(utc_time_str):
    if '.' in utc_time_str:
        timestamp_utc = time.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        timestamp_utc = time.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    timestamp = time.mktime(timestamp_utc) + 3600 * 8
    return timestamp

def localtime_to_beijing_timestamp(local_time_str):
    return time.mktime(time.strptime(local_time_str, TIME_PATTERN["text"]))

def timestamp_to_standard_time(timestamp):
    if timestamp:
        standard_time = time.strftime(TIME_PATTERN["timestamp"], time.localtime(float(timestamp)))
        return standard_time
    return timestamp

def convert_to_time(time_str, pattern='default'):
    return datetime.strptime(time_str, TIME_PATTERN["timestamp"])

def convert_to_timestamp(time_str):
    return convert_to_time(time_str).timestamp()
    
def get_closest_timestamp(timestamp, target_timestamps):
    _target_timestamps = [abs(convert_to_timestamp(timestamp) - convert_to_timestamp(t)) for t in target_timestamps]
    
    return target_timestamps[_target_timestamps.index(min(_target_timestamps))]

# -----Text-----
def file_include_str_last_line(str, file_path):
    num = 0
    try:
        if os.path.exists(file_path):
            cmd = 'grep -a -n "{}" {}'.format(str, file_path) + " | awk -F ':' '{print $1}' | tail -n 1"
            res = shell_execute(cmd)
            result = res[1]
            if result:
                num = int(result)
            # print('line_num:', num)
    except BaseException as e:
        print(e)
    return num

def Red(msg):           return "\033[91m {}\033[00m".format(msg)
def Green(msg):         return "\033[92m {}\033[00m".format(msg)
def Yellow(msg):        return "\033[93m {}\033[00m".format(msg)
def LightPurple(msg):   return "\033[94m {}\033[00m".format(msg)
def Purple(msg):        return "\033[95m {}\033[00m".format(msg)
def Cyan(msg):          return "\033[96m {}\033[00m".format(msg)
def LightGray(msg):     return "\033[97m {}\033[00m".format(msg)
def Black(msg):         return "\033[98m {}\033[00m".format(msg)

# -----File-----
def get_log_timestamp_list(timestamps = None, critical = True):
    if not timestamps:
        cmd = f"ls -l {LOG_DIR} | grep 2023 | awk '{{print $9}}'"
        res = shell_execute(cmd, critical)
        timestamps = [[timestamp.strip(), timestamp.strip()] for timestamp in res[1].split()]
        if critical and not timestamps:
            print("[ERROR] Logs directory empty, load failure")
            sys.exit()
    return timestamps

def get_log_last_timestamp(timestamp = None, critical = True):
    if not timestamp:
        cmd = f"ls -l {LOG_DIR} | grep 2023 | awk '{{print $9}}' | tail -n 1"
        res = shell_execute(cmd, critical)
        timestamp = res[1]
        if critical and not timestamp:
            print("[ERROR] Logs directory empty, load failure")
            sys.exit()
    return timestamp

def get_json_info(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        json_dict = json.load(f)
    return json_dict

def get_yaml_info(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        yaml_dict = yaml.load(f, yaml.FullLoader)
    return yaml_dict

def write_data_to_file(content, filepath):
    with open(filepath, mode='a', encoding='utf-8') as f:
        f.write(content)
        f.write('\n')

def write_data_to_csv(content, csv_file_path):
    with open(csv_file_path, mode='a', newline='\n') as f:
        ob_csv = csv.writer(f)
        ob_csv.writerow(content)

def get_value_by_field(field, filepath, flag=True):
    # keyword: field. flag=True: Get the row where the keyword is located, otherwise get the next row
    # TODO 串行(hang)的情况下awk可能会漏取值
    ret = None
    if flag:
        cmd = "grep '{}' {}".format(field, filepath) + " | awk -F ':' '{print $2}'"
        res = shell_execute(cmd)
        ret = res[1]
    else:
        cmd = "grep -n '{}' {} ".format(field, filepath) + " |  awk -F ':' '{print $1}'"
        res = shell_execute(cmd)
        line_num = res[1]
        if line_num:
            next_line_num = int(line_num) + 1
            cmd = "sed -n '{}p' {}".format(next_line_num, filepath)
            res = shell_execute(cmd)
            ret = res[1]
    return ret

# -----Env-----
def escalate_previlege(user: str, passwd: str):
    workdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cmd = f'echo {passwd} | sudo -S chown -R {user}:users {workdir}'
    shell_execute(cmd)

def set_logpath(logdir='.', subdir=''):
    logpath = os.path.join(str(logdir), str(subdir).strip())
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    return logpath

def save_variable(v, filename):
    with open(filename, 'wb') as f:
        pickle.dump(v, f)
    return filename

def load_variable(filename):
    with open(filename, 'rb') as f:
        v = pickle.load(f)
    return v

def shell_execute(cmd, critical = True):
    # critical为True时，命令执行出错则会抛出异常
    retry_time = CMD_RETRY_TIME
    while retry_time > 0:
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = p.returncode
        output = p.stdout.decode().strip() # decode("utf-8")
        error = p.stderr.decode().strip()
        if ret == 0:
            return [ret, output]
        retry_time -= 1
    print(f'[ERROR] Command "{cmd}" failed executing, code {ret}, errmsg "{error}"')
    # LOGGER.error(f'Command "{cmd}" failed executing for {CMD_RETRY_TIME} times, code {ret}, errmsg "{error}"')
    if critical:
        raise subprocess.CalledProcessError
    return [ret, error]

def args_parser():
    parser = argparse.ArgumentParser(description='Parser for generating stressing pod')
    parser.add_argument('-G', '--generate', 
                        default=False, action="store_true", 
                        help='从csv生成workload')
    parser.add_argument('-T', '--watch_time', type=str, 
                        default=600, 
                        help='测试持续时间，默认为10分钟')
    parser.add_argument('-RM', '--running_mode', type=str, 
                        default='local', choices=['local', 'remote', 'mixed'], 
                        help='本地或拉远，默认为local')
    args = parser.parse_args()
    return args
