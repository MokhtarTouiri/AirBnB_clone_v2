#!/usr/bin/python3
"""
Write a Fabric script that generates a .tgz
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    date = datetime.now().strftime('%Y%m%d%H%M%S')
    local('sudo mkdir versions')
    directory = 'versions/web_static_{}.tgz'.format(date)
    local('tar -cvzf {} web_static/'.format(directory))
    return directory
