#! /usr/bin/python

import requests
import os
import urllib.request
import json
import re
import imghdr
import sys

if "test" in sys.argv:
    from gi.repository import Gio

__author__ = 'z3ntu'

SCHEMA = 'org.gnome.desktop.background'
KEY = 'picture-uri'
ROOT_PATH = os.path.expanduser('~/.earthpornwallpaper/')
DOWNLOAD_PATH = ROOT_PATH + "downloads/"
TMP_PATH = ROOT_PATH + "tmp/"
IMGUR_BASE = "http://i.imgur.com/%IMGURID%.jpg"

FILES = [str] * 3

PICDURATION = "120,00"
TRANSITIONDURATION = "3,00"


def main():
    filecounter = 0

    create_directories()
    clean_directory(DOWNLOAD_PATH)
    clean_directory(TMP_PATH)

    # PREPARE AND EXECUTE HTTP GET REQUEST
    payload = {'limit': 5}
    headers = {'user-agent': 'EarthPornWallpaper'}
    r = requests.get("http://www.reddit.com/r/earthporn.json", params=payload, headers=headers)

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
            
        if save_img(url, filecounter):
            print("Successful save!")
            filecounter += 1

        if filecounter >= 3:
            break

    write_xml(True)
    return


def save_img(url, filecounter):
    tmp_path = TMP_PATH + "tmp" + str(filecounter)

    print("Saving " + url + " as " + tmp_path)
    resource = urllib.request.urlopen(url)
    output = open(tmp_path, "wb")
    output.write(resource.read())
    output.close()

    imgtype = imghdr.what(tmp_path)
    if imgtype is None:
        print("Not a valid image, skipping!")
        return False

    new_path = DOWNLOAD_PATH + "download" + str(filecounter) + "." + imgtype
    os.rename(tmp_path, new_path)
    print("Moved to " + new_path)
    FILES[filecounter] = new_path
    return True


def create_directories():
    print("Creating directories")
    os.makedirs(ROOT_PATH, exist_ok=True)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(TMP_PATH, exist_ok=True)
    return


def clean_directory(path):
    print("Cleaning directory " + path)
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                return True
        except Exception:
            print("exception while cleaning downloads directory!")
    return False


def clean_xml():
    print("Cleaning XML file")
    xmlpath = ROOT_PATH + "wallpaper.xml"
    delete_file(xmlpath)


def delete_file(path):
    if os.path.isfile(path):
        os.unlink(path)
        return True
    return False


def write_xml(setlocation):
    clean_xml()
    print("Writing XML file")
    r = open("wallpaper_template.xml", "r")
    template = r.read()
    r.close()
    template = template.replace("%FILE1%", FILES[0])
    template = template.replace("%FILE2%", FILES[1])
    template = template.replace("%FILE3%", FILES[2])
    template = template.replace("%TRANSITIONDURATION%", TRANSITIONDURATION)
    template = template.replace("%PICDURATION%", PICDURATION)
    w = open(ROOT_PATH + "wallpaper.xml", "w")
    w.write(template)
    w.close()
    if setlocation:
        set_wallpaper_location(ROOT_PATH + "wallpaper.xml")


def set_wallpaper_location(filepath):
    if "test" in sys.argv:
        gsettings = Gio.Settings.new(SCHEMA)
        gsettings.set_string(KEY, "file://" + filepath)


if __name__ == '__main__':
    main()
