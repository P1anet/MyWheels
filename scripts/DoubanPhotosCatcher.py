from bs4 import BeautifulSoup
import requests
import os
import time
import sys
import tkinter as tk
from tkinter import filedialog
import logging
import json

# critical > error > warning > info > debug
LOGGER_NAME = "basic_logger"
LOG_LEVEL = logging.INFO
LOG_FORMATTER = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s', "%Y-%m-%d %H:%M:%S")
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(LOG_LEVEL)

# headers = {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 Edg/99.0.4844.51"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
retry_limits = 5
photos_per_page = 30
name_nosuffix = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]

class DoubanPhotosCatcher:
    def __init__(self, url, d_path, cache, name = None):
        self.__url = url
        self.__d_path = d_path
        self.__category = self.__url.split("/")[3]
        self.__id = self.__url.split("/")[4]
        if name:
            self.__id = name
        self.__name = f'{self.__category}/{self.__id}'
        self.__cacheUrls = cache.get(self.__name, [])
        self.__downloadUrls = []
        self.__failedUrls = []

    def run(self):
        LOGGER.info(f"Getting photos from {self.__url}")
        r = requests.get(self.__url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        pageNum = soup.select('.paginator a')[-2].text
        pageSize = photos_per_page
        index = 0
        while index < int(pageNum):
            url = self.__url + '?type=C&start=' + str(index * pageSize) + '&sortby=like&size=a&subtype=a'
            self.parse(url)
            index += 1
            LOGGER.info(f"Collecting urls of photos on Page {str(index)} success")
        self.download()
        if len(self.__failedUrls):
            LOGGER.warning(f"Failed urls: {str(self.__failedUrls)}")
        LOGGER.info(f'Completed: Cached {len(self.__cacheUrls)}, Downloaded {len(self.__downloadUrls)}, Failed {len(self.__failedUrls)}')
    
    def parse(self, url):
        r = requests.get(url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        imgTags = soup.select('#wrapper #content .cover img')
        for tag in imgTags:
            if tag['src'] not in self.__cacheUrls:
                self.__downloadUrls.append(tag['src'])
        
    def download(self):
        dir_path = os.path.join(self.__d_path, self.__category, self.__id)
        os.makedirs(dir_path, exist_ok=True)
        LOGGER.info("Start downloading")
        LOGGER.info(f"Saving photos in {dir_path}")
        size = len(self.__downloadUrls)
        i = 0
        while i < size:
            file_name = f"{str(i)}.jpg"
            file_path = os.path.join(dir_path, file_name)
            url = self.__downloadUrls[i]
            r = requests.get(url, headers=headers)
            retry = 1
            while not r.ok:
                r = requests.get(url, headers=headers)
                retry += 1
                if retry > retry_limits:
                    LOGGER.warning(f"Failed downloading {url}, please download manually")
                    self.__failedUrls.append(url)
                    continue
                time.sleep(1)
            LOGGER.info(f"Downloading {file_name} after {retry} requests. Url: {url}. Path: {file_path}")
            with open(file_path, 'wb') as f:
                f.write(r.content)
            i += 1
            if i % 5 == 0:
                time.sleep(1)


if __name__ == '__main__':
    # 实例化tk
    root = tk.Tk()
    root.withdraw()
    # 指定保存文件夹路径
    d_path = filedialog.askdirectory()
    # f_path = filedialog.askopenfilename()
    CACHE_PATH = os.path.join(d_path, "cache.json")
    cache = {}
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, mode='r', encoding='utf-8') as f:
            cache = json.load(f)
    # 记录日志路径
    LOG_PATH = os.path.join(d_path, f'{name_nosuffix}.txt')
    # FileHandler
    FH = logging.FileHandler(LOG_PATH)
    FH.setLevel(LOG_LEVEL)
    FH.setFormatter(LOG_FORMATTER)
    LOGGER.addHandler(FH)
    # StreamHandler
    SH = logging.StreamHandler()
    SH.setLevel(LOG_LEVEL)
    SH.setFormatter(LOG_FORMATTER)
    LOGGER.addHandler(SH)
    # 指定相册url
    # url = "https://movie.douban.com/subject/33447346/photos"
    # url = sys.argv[1]
    # urls = [url]
    # urls = [
    #     "https://movie.douban.com/celebrity/1430482/photos",
    #     "https://movie.douban.com/celebrity/1350633/photos",
    #     "https://movie.douban.com/subject/33447346/photos",
    #     "https://movie.douban.com/subject/35031404/photos",
    #     "https://movie.douban.com/subject/35465737/photos",
    #     "https://movie.douban.com/subject/35907659/photos"
    # ]
    # urls = {
    #     "Rafael Silva":         "https://movie.douban.com/celebrity/1430482/photos",
    #     "Ronen Rubinstein":     "https://movie.douban.com/celebrity/1350633/photos",
    #     "S01":                  "https://movie.douban.com/subject/33447346/photos",
    #     "S02":                  "https://movie.douban.com/subject/35031404/photos",
    #     "S03":                  "https://movie.douban.com/subject/35465737/photos",
    #     "S04":                  "https://movie.douban.com/subject/35907659/photos"
    # }
    urls = {
        "Alan Ritchson":        "https://movie.douban.com/celebrity/1254642/photos"
    }
    sources = cache.get("sources", {})
    for name, url in urls.items():
        LOGGER.info("=" * 20)
        sources.update(urls)
        catcher = DoubanPhotosCatcher(url, d_path, cache, name)
        catcher.run()
        cache[catcher._DoubanPhotosCatcher__name] = catcher._DoubanPhotosCatcher__cacheUrls + catcher._DoubanPhotosCatcher__downloadUrls
    cache["sources"] = sources
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)
