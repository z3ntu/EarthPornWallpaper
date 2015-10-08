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

FILES = [str] * 3

PICDURATION = "120,00"
TRANSITIONDURATION = "3,00"


def main():
    FILECOUNTER = 0

    create_directories()
    clean_download_directory()

    # PREPARE AND EXECUTE HTTP GET REQUEST
    payload = {'limit': 3}
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

        # print(url)
        save_img(url, FILECOUNTER)
        FILECOUNTER += 1

    write_xml(True)
    return


def save_img(url, filecounter):
    print("Saving " + url + " as download" + str(filecounter))
    resource = urllib.request.urlopen(url)
    output = open(DOWNLOAD_PATH + "download" + str(filecounter), "wb")
    output.write(resource.read())
    output.close()
    newfilename = "download" + str(filecounter) + "." + imghdr.what(DOWNLOAD_PATH + "download" + str(filecounter))
    os.rename(DOWNLOAD_PATH + "download" + str(filecounter), DOWNLOAD_PATH + newfilename)
    print("Renamed to " + newfilename)
    FILES[filecounter] = DOWNLOAD_PATH + newfilename
    return


def create_directories():
    print("Creating directories")
    os.makedirs(ROOT_PATH, exist_ok=True)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    return


def clean_download_directory():
    print("Cleaning download directory.")
    for the_file in os.listdir(DOWNLOAD_PATH):
        file_path = os.path.join(DOWNLOAD_PATH, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            print("exception while cleaning downloads directory!")
    return


def clean_xml():
    print("Cleaning XML file")
    xmlpath = ROOT_PATH + "wallpaper.xml"
    if os.path.isfile(xmlpath):
        os.unlink(xmlpath)


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
    # SET BACKGROUND
    gsettings = Gio.Settings.new(SCHEMA)
    gsettings.set_string(KEY, "file://" + filepath)


if __name__ == '__main__':
    main()
