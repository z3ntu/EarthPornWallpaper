#! /usr/bin/python

from gi.repository import Gio
import requests
import os
import urllib.request
import json
import re
import imghdr

__author__ = 'z3ntu'

SCHEMA = 'org.gnome.desktop.background'
KEY = 'picture-uri'
ROOT_PATH = os.path.expanduser('~/.earthpornwallpaper/')
DOWNLOAD_PATH = ROOT_PATH + "downloads/"
IMGUR_BASE = "http://i.imgur.com/%IMGURID%.jpg"


def main():
    filecounter = 0
    create_directories()
    clean_download_directory()

    # PREPARE AND EXECUTE HTTP GET REQUEST
    payload = {'limit': 3}
    headers = {'user-agent': 'EarthPornWallpaper'}
    r = requests.get("http://www.reddit.com/r/earthporn.json", params=payload, headers=headers)

    # SET BACKGROUND
    gsettings = Gio.Settings.new(SCHEMA)
    # gsettings.set_string(KEY, "file://" + background)

    # PARSE JSON
    redditapi = json.loads(r.text)
    children = redditapi['data']['children']
    for item in children:
        url = item['data']['url']

        # CHECK IF IMGUR LINK (non-direct)
        imgur = re.search('://imgur.com/', url)
        if imgur:
            imgurid = url[imgur.end()::]
            url = IMGUR_BASE.replace("%IMGURID%", imgurid)

        # print(url)
        save_img(url, "download" + str(filecounter))
        filecounter += 1

    return


def save_img(url, filename):
    print("Saving " + url + " as " + filename)
    resource = urllib.request.urlopen(url)
    output = open(DOWNLOAD_PATH + filename, "wb")
    output.write(resource.read())
    output.close()
    newfilename = filename + "." + imghdr.what(DOWNLOAD_PATH + filename)
    os.rename(DOWNLOAD_PATH + filename, DOWNLOAD_PATH + newfilename)
    print("Renamed to " + newfilename)
    return


def create_directories():
    os.makedirs(ROOT_PATH, exist_ok=True)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    return


def clean_download_directory():
    for the_file in os.listdir(DOWNLOAD_PATH):
        file_path = os.path.join(DOWNLOAD_PATH, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            print("exception while cleaning downloads directory!")
    return


if __name__ == '__main__':
    main()
