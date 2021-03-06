#!/usr/bin/python3

import requests
import os
import urllib.request
import json
import re
import imghdr
import sys
import libdesktop.wallpaper as lw
from time import strftime

__author__ = 'z3ntu'

# SCHEMA = 'org.gnome.desktop.background'
# KEY = 'picture-uri'
DATA_PATH = os.path.expanduser('~/.local/share/earthpornwallpaper/')
DOWNLOAD_PATH = DATA_PATH + "downloads/"
TMP_PATH = DATA_PATH + "tmp/"
IMGUR_BASE = "http://i.imgur.com/%IMGURID%.jpg"
LOG_FILE = DATA_PATH + "output.log"
LOG = sys.__stdout__

FILES = [str] * 3

PICDURATION = "120,00"
TRANSITIONDURATION = "3,00"

HEADER = {'user-agent': 'EarthPornWallpaper'}


def main():
    global LOG
    LOG = open(LOG_FILE, "a")
    log("------- BEGIN EARTHPORNWALLPAPER -------")
    filecounter = 0

    create_directories()
    clean_directories()

    # PREPARE AND EXECUTE HTTP GET REQUEST
    payload = {'limit': 5}
    r = requests.get("http://www.reddit.com/r/earthporn.json", params=payload, headers=HEADER)

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
            log("Successful save!")
            filecounter += 1

        if filecounter >= 3:
            break

    # write_xml(True)
#    set_wallpaper()
    return


def save_img(url, filecounter):
    tmp_path = TMP_PATH + "tmp" + str(filecounter)

    log("Saving " + url + " as " + tmp_path)
    request = urllib.request.Request(url, headers=HEADER)
    resource = urllib.request.urlopen(request)
    output = open(tmp_path, "wb")
    output.write(resource.read())
    output.close()

    imgtype = imghdr.what(tmp_path)
    if imgtype is None:
        log("Not a valid image, skipping!")
        return False

    new_path = DOWNLOAD_PATH + "download" + str(filecounter) + "." + imgtype
    os.rename(tmp_path, new_path)
    log("Moved to " + new_path)
    FILES[filecounter] = new_path
    return True


def create_directories():
    log("Creating directories")
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(TMP_PATH, exist_ok=True)
    return


def clean_directory(path):
    log("Cleaning directory " + path)
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                return True
        except OSError:
            log("exception while cleaning directory " + path)
    return False


def clean_directories():
    clean_directory(DOWNLOAD_PATH)
    clean_directory(TMP_PATH)


def clean_xml():
    log("Cleaning XML file")
    xmlpath = DATA_PATH + "wallpaper.xml"
    delete_file(xmlpath)


def delete_file(path):
    if os.path.isfile(path):
        os.unlink(path)
        return True
    return False


# def write_xml(setlocation):
#     clean_xml()
#     log("Writing XML file")
#     r = open(DATA_PATH + "wallpaper_template.xml", "r")
#     template = r.read()
#     r.close()
#     template = template.replace("%FILE1%", FILES[0])
#     template = template.replace("%FILE2%", FILES[1])
#     template = template.replace("%FILE3%", FILES[2])
#     template = template.replace("%TRANSITIONDURATION%", TRANSITIONDURATION)
#     template = template.replace("%PICDURATION%", PICDURATION)
#     w = open(DATA_PATH + "wallpaper.xml", "w")
#     w.write(template)
#     w.close()
#     if setlocation:
#         set_wallpaper_location(DATA_PATH + "wallpaper.xml")

def set_wallpaper():
#    if os.environ.get("KDE_FULL_SESSION") == "true":
#        command = """
#        qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
#            var allDesktops = desktops();
#            print (allDesktops);
#            for (i=0;i<allDesktops.length;i++) {{
#                d = allDesktops[i];
#                d.wallpaperPlugin = "org.kde.image";
#                d.currentConfigGroup = Array("Wallpaper",
#                                             "org.kde.image",
#                                             "General");
#                d.writeConfig("Image", "file:///{save_location}")
#            }}
#        '
#        """
#        # TODO: Slideshow with plugin "org.kde.slideshow" -> "SlidePaths=/home/luca/.local/share/earthpornwallpaper/downloads/"
#        os.system(command.format(save_location=FILES[0]))
#    else:
        lw.set(FILES[0])




# def set_wallpaper_location(filepath):
#     if "test" not in sys.argv:
#         from gi.repository import Gio
#         gsettings = Gio.Settings.new(SCHEMA)
#         gsettings.set_string(KEY, "file://" + filepath)


def log(message):
    if "cron" not in sys.argv:
        print("[" + strftime("%Y-%m-%d %H:%M:%S") + "] " + message)
    LOG.write("[" + strftime("%Y-%m-%d %H:%M:%S") + "] " + message + "\n")

if __name__ == '__main__':
    main()
