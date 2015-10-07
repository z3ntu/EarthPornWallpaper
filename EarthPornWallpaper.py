#! /usr/bin/python

from gi.repository import Gio
import requests
import os

__author__ = 'luca'
SCHEMA = 'org.gnome.desktop.background'
KEY = 'picture-uri'

path = os.path.expanduser('~/.earthpornwallpaper')
os.makedirs(path, exist_ok=True)

payload = {'limit': 3}
headers = {'user-agent': 'EarthPornWallpaper'}

r = requests.get("http://www.reddit.com/r/earthporn.json", params=payload, headers=headers)

gsettings = Gio.Settings.new(SCHEMA)
# gsettings.set_string(KEY, "file://" + background)


print(r.json())
