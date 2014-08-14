from fabric.api import *
import os

def up(port="8007"):
    local("python manage.py runserver 0.0.0.0:%s"%port)

