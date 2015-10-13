#!/usr/bin/python3

import os
import shutil
from pwd import getpwnam
from earthpornwallpaper import create_directories, clean_directories, delete_file, log

DATA_PATH = os.path.expanduser('~/.earthpornwallpaper/')
DOWNLOAD_PATH = DATA_PATH + "downloads/"
TMP_PATH = DATA_PATH + "tmp/"


def main():
    # 2. Create directories and remove files
    create_directories()
    clean_directories()
    delete_file(DATA_PATH + "wallpaper_template.xml")
    delete_file(DATA_PATH + "wallpaper.xml")
    log("Created directories")

    # 3. Copy template to appropriate folder
    shutil.copy("wallpaper_template.xml", DATA_PATH)
    os.chown(DATA_PATH + "wallpaper_template.xml", getpwnam(os.getlogin()).pw_uid, -1)
    os.chmod(DATA_PATH + "wallpaper_template.xml", 0o444)
    log("Copied template to the right folder")


if __name__ == '__main__':
    main()
