#!/usr/bin/python3

import os
import shutil
import sys
from pwd import getpwnam
from time import strftime
from earthpornwallpaper import create_directories, clean_directories, delete_file

DATA_PATH = os.path.expanduser('~/.local/share/earthpornwallpaper/')
DOWNLOAD_PATH = DATA_PATH + "downloads/"
TMP_PATH = DATA_PATH + "tmp/"
PROGRAM_PATH = "/usr/local/bin/"
CRONTAB_FILE = "/etc/cron.d/earthpornwallpaper"

CRONTAB_CONTENT = "# DO NOT CHANGE THIS FILE!\n" \
                  "# CREATED BY EARTHPORNWALLPAPER\n" \
                  "# https://github.com/z3ntu/EarthPornWallpaper\n" \
                  "\n" \
                  "# minute hour day month dayOfWeek user command\n" \
                  "0 * * * * " + os.getlogin() + " " + "earthpornwallpaper cron"


def main():
    if not check_if_root():
        sys.exit("Please run the setup as root!")

    # 1. Copy script to /usr/local/bin
    shutil.copy("earthpornwallpaper.py", PROGRAM_PATH + "earthpornwallpaper")
    os.chmod(PROGRAM_PATH + "earthpornwallpaper", 0o755)
    log("Copied script")

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

    # 4. Create cronjob entry
    crontab = open(CRONTAB_FILE, "w")
    crontab.write(CRONTAB_CONTENT)
    crontab.close()
    log("Written cronjob!")


def log(message):
    print("[" + strftime("%Y-%m-%d %H:%M:%S") + "] " + message)


def check_if_root():
    return os.geteuid() == 0


if __name__ == '__main__':
    main()
