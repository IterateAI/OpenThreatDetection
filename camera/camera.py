import json
from collections import namedtuple
from json import JSONEncoder
from string import Template
from flask import Blueprint, render_template,current_app,jsonify,Response,request
from config import db
from bson import ObjectId 
import cv2

camera_bp = Blueprint('camera_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets')

class Camera:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

cameras = []
rtsp_url='http://localhost:8000/video'

def init():
    try:
        collection = db.db['camera']
        global cameras
        cameras_objs = list(collection.find())
        for item in cameras_objs:
            item['_id'] = str(item['_id'])
        print("json conversion done",cameras_objs)
        
        cameras = [Camera(**camera_dict) for camera_dict in cameras_objs]

        print(cameras)
        
        for camera in cameras:
            with open("config/wep_ini_template.txt", "r") as init_template_file:
                print(f"creating wep ini file for camera {camera.name}")
                t = Template(init_template_file.read())
                x = t.substitute(name=camera.name, location=camera.location, type=camera.link_type, link=camera.link, frame_size=camera.frame_skip_size)
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

def cameras_to_json():
    try:
        collection = db.db['camera']
        data = list(collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
    #for camera in cameras:
    #    print(json.dumps(camera.__dict__))
    # return json.loads(json.dumps(cameras, default = lambda x: x.__dict__))

@camera_bp.route('/')
def home():
    return render_template("camera/camera.html", cameras=cameras)

@camera_bp.route('/cameras')
def get_cameras_as_json():
    return cameras_to_json()

@camera_bp.route('/cameras/add', methods=["POST"])
def store_camera_config():
    data = request.get_json()
    print(data)

    # Ensure that the JSON request contains the necessary fields
    if 'link' not in data or 'link_type' not in data:
        return jsonify({'message': 'Missing camera_id or config field in request'}), 400

    # Store the camera configuration in MongoDB
    try:
        camera_configs = db.db["camera"]
        camera_configs.insert_one(data)
        return jsonify({'message': 'Camera configuration stored successfully'}), 201
    except Exception as e:
        print(str(e))
        return jsonify({'message': str(e)}), 500

@camera_bp.route("/cameras/<string:camera_id>", methods=["GET"])
def get_camera_configuration(camera_id):
    print(camera_id)
    camera = db.db['camera'].find({"_id": ObjectId(str(camera_id))})
    
    if camera:
        data = list(camera)
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    return "Camera not found", 404    

@camera_bp.route('/cameras/update/<string:camera_id>', methods=['PUT'])
def edit_camera_configuration(camera_id):
    try:
        # Get data from the request JSON
        data = request.json
        

        # camera_id = data.get("camera_id")
        updated_fields = data.get("updated_fields")
        print(updated_fields,camera_id)
        # Check if the camera ID and updated fields are provided
        if not updated_fields:
            print("no update fileds")
            return jsonify({"message": "Missing camera_id or updated_fields"}), 400

        # Update the specified camera configuration document
        result = db.db['camera'].update_one({"_id": ObjectId(str(camera_id))}, {"$set": updated_fields})
        # print(list(result))
        # Check if the update was successful
        if result.matched_count == 0:
            return jsonify({"message": "Camera not found"}), 404

        return jsonify({"message": "Camera configuration updated successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
