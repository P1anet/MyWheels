#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
批量修改照片文件名称的Python脚本程序。
遍历指定目录（含子目录）的照片文件，根据拍照时间将照片文件名修改为以下格式：
20140315_091230.jpg (%Y%m%d_%H%M%S)
由于文件名已经精确到秒，理论上重名的概率非常小。
如果需要考虑到重名的问题，可以对本程序进行进一步的优化。
！该程序需要安装exifread模块，否则无法使用。
例如，Linux/Mac OS X下命令行安装该模块：sudo pip install exifread
'''

import os
import stat
import time
import exifread
import json
from pymediainfo import MediaInfo
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog


MY_DATE_FORMAT = '%Y%m%d_%H%M%S'
DELETE_FILES  = ['thumbs.db', 'sample.dat']
DELETE_FILTER = []
PIC_FILTER    = ['.jpg', '.bmp', '.jpeg', '.heic', '.png', '.dng', '.arw', '.gif']
MOVIE_FILTER  = ['.mp4', '.avi', '.mov', '.mpg', '.mpeg']
PIC_CONF_FILETER  = ['.xmp']
MOVIE_CONF_FILTER = ['.xml', '.thm']
SUFFIX_FILTER = MOVIE_FILTER + PIC_FILTER


def isPicFileType(filename):
    # 根据文件扩展名，判断是否是需要处理的文件类型
    filename_nopath = os.path.basename(filename)
    f, e = os.path.splitext(filename_nopath)
    return e.lower() in PIC_FILTER


def isMovieFileType(filename):
    # 根据文件扩展名，判断是否是需要处理的文件类型
    filename_nopath = os.path.basename(filename)
    f, e = os.path.splitext(filename_nopath)
    return e.lower() in MOVIE_FILTER


def isFormatedFileName(filename):
    # 判断是否已经是格式化过的文件名
    try:
        filename_nopath = os.path.basename(filename)
        f, e = os.path.splitext(filename_nopath)
        time.strptime(f, MY_DATE_FORMAT)
        return True
    except ValueError:
        return False


def isTargetedFileType(filename):
    # 根据文件扩展名，判断是否是需要处理的文件类型
    filename_nopath = os.path.basename(filename)
    f, e = os.path.splitext(filename_nopath)
    return e.lower() in SUFFIX_FILTER


def isDeleteFile(filename):
    # 判断是否是指定要删除的文件
    filename_nopath = os.path.basename(filename)
    f, e = os.path.splitext(filename_nopath)
    return filename_nopath.lower() in DELETE_FILES or e.lower() in DELETE_FILTER


# 取媒体生成日期
def getFileDate(filepath, format):
    media_info = MediaInfo.parse(filepath)
    data = media_info.to_json()
    d = json.loads(data)
    x = d.get("tracks")
    temp_time = (x[0].get("comapplequicktimecreationdate"))
    beijing_time = ""
    if temp_time:
        temp_time = temp_time.replace("UTC ", "")
        temp_time = temp_time.replace("T", " ")
        temp_time = temp_time.replace("+0800", "")
        beijing_time = datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S")
        return str(beijing_time)
    else:
        temp_time = (x[0].get("encoded_date"))
        if temp_time is None:
            temp_time = (x[0].get("file_last_modification_date")).split('.')[0]
        temp_time = temp_time.replace("UTC ", "")
        beijing_time = datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
        return str(beijing_time)


def generateNewFileName(filename):
    dateStr = ""
    # 如果是图片
    if isPicFileType(filename):
        # 根据照片的拍照时间生成新的文件名（如果获取不到拍照时间，则使用文件的创建时间）
        dateStr = ""
        try:
            if os.path.isfile(filename):
                fd = open(filename, 'rb')
            else:
                raise "[%s] is not a file!\n" % filename
        except:
            raise "unopen file[%s]\n" % filename
        try:
            data = exifread.process_file(fd)
        except:
            data = None
        FIELD = 'EXIF DateTimeOriginal'

        if data and (FIELD in data):
            # print("\nstr(data[FIELD]): %s" %(str(data[FIELD])))  # 获取到的结果格式类似为：2018:12:07 03:10:34
            # print("\nstr(data[FIELD]).replace(':', '').replace(' ', '_'): %s" %(str(data[FIELD]).replace(':', '').replace(' ', '_'))) # 获取结果格式类似为：20181207_031034
            # print("\nos.path.splitext(filename)[1]: %s" %(os.path.splitext(filename)[1]))  # 获取了图片的格式，结果类似为：.jpg
            new_name = str(data[FIELD]).replace(':', '').replace(
                ' ', '_') + os.path.splitext(filename)[1]
            # print("\nnew_name: %s" %(new_name)) # 20181207_031034.jpg

            time1 = new_name.split(".")[0][:13]
            new_name2 = new_name.split(".")[0][:8] + '_' + filename
            # print("\nfilename: %s" %filename)
            # print("\n%s的拍摄时间是: %s年%s月%s日%s时%s分" % (filename, time1[0:4], time1[4:6], time1[6:8], time1[9:11], time1[11:13]))

            dateStr = str(data[FIELD])
            dateStr = dateStr.replace(
                "-", "").replace(":", "").replace("/", "").replace(" ", "_")
        # 如果没有取得exif信息，则用图像文件的创建日期作为拍摄日期
        if dateStr == "":
            state = os.stat(filename)
            dateStr = time.strftime(MY_DATE_FORMAT, time.localtime(state[-2]))

    # 如果是视频
    elif isMovieFileType(filename):
        # 取媒体生成日期
        dateStr = str(getFileDate(filename, MY_DATE_FORMAT))
        dateStr = dateStr.replace("-", "").replace(":", "").replace(" ", "_")
    else:
        pass

    dirname = os.path.dirname(filename)
    filename_nopath = os.path.basename(filename)
    f, e = os.path.splitext(filename_nopath)
    newFileName = os.path.join(dirname, dateStr + e).lower()
    return newFileName


def renameFile(file, filename):
    print("rename [%s] => [%s]" % (file, filename))
    os.rename(file, filename)


def isCompatible(dstFile, srcFile):
    if dstFile == srcFile or dstFile == srcFile + 'M01':
        return True
    return False


def renameAttachedFile(file, filename):
    filter = []
    if isPicFileType(file):
        filter = PIC_CONF_FILETER
    elif isMovieFileType(file):
        filter = MOVIE_CONF_FILTER
    else:
        pass
    f, e = os.path.splitext(file)
    dirname = os.path.dirname(filename)
    filename_nopath = os.path.basename(filename)
    nf, ne = os.path.splitext(filename_nopath)
    for obj in os.listdir(os.curdir):
        _f, _e = os.path.splitext(obj)
        if isCompatible(_f, f) and _e.lower() in filter:
            newFileName = os.path.join(dirname, nf + _e).lower()
            renameFile(obj, newFileName)


def scandir(startdir):
    # 遍历指定目录以及子目录，对满足条件的文件进行改名或删除处理
    os.chdir(startdir)
    print("====================================================")
    print("Current working directory:", os.getcwd())
    for obj in os.listdir(os.curdir):
        if os.path.isfile(obj):
            if isTargetedFileType(obj) and isFormatedFileName(obj) == False:
                # 对满足过滤条件的文件进行改名处理
                newFileName = generateNewFileName(obj)
                # print("newFileName:" + newFileName)
                if not os.path.exists(newFileName):
                    renameFile(obj, newFileName)
                else:
                    filename_nopath = os.path.basename(newFileName)
                    f, e = os.path.splitext(filename_nopath)
                    for i in range(100):
                        newFileName = f + "(" + str(i) + ")" + e
                        if not os.path.exists(newFileName):
                            renameFile(obj, newFileName)
                            break
                renameAttachedFile(obj, newFileName)
                

            elif isDeleteFile(obj):
                # 删除制定的文件
                print("delete [%s]: " % obj)
                os.remove(obj)
            else:
                pass
        elif os.path.isdir(obj):
            scandir(obj)
        else:
            pass
    os.chdir(os.pardir)


if __name__ == "__main__":
    # 实例化tk
    root = tk.Tk()
    root.withdraw()
    # 获取文件夹路径
    d_path = filedialog.askdirectory()
    # f_path = filedialog.askopenfilenames()
    # 扫描路径
    scandir(d_path)
