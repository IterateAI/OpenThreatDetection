import json
from collections import namedtuple
from json import JSONEncoder
from string import Template
from flask import  render_template,current_app,jsonify,Response,request
from extenstions import db
from bson import ObjectId 
from .models import Camera
from app import app

class Cameras:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

cameras = []

def init():
    try:
        with app.app_context():
            collection = Camera.query.all() 
            global cameras
            cameras=collection
        for camera in cameras:
            with open("config/wep_ini_template.txt", "r") as init_template_file:
                print(f"creating wep ini file for camera {camera.name}")
                t = Template(init_template_file.read())
                x = t.substitute(name=camera.name, location=camera.location, type=camera.video_type, link=camera.video_link, frame_size=camera.frame_skip_size)
                init_file = open(f"config/wep_{camera.name}.ini", "w")
                init_file.write(x)
                init_file.close()
            with open("config/weplog_template.txt", "r") as weplog_template_file:
                print(f"creating wep log config file for camera {camera.name}")
                t = Template(weplog_template_file.read())
                x = t.substitute(camera=camera.name)
                log_file = open(f"config/weplog_{camera.name}.conf", "w")
                log_file.write(x)
                log_file.close()

    except Exception as e:
        return jsonify({"error": str(e)})


def get_cameras():
    return cameras

def to_camera_ini_name(camera):
    return f"config/wep_{camera.name}.ini"
