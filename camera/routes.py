from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from .models import Camera
from extenstions import db


camera_bp = Blueprint('camera_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets')

@camera_bp.route('/')
def home():
    cameras = Camera.query.all() 
    return render_template("camera/camera.html", cameras=cameras)

@camera_bp.route('/cameras')
def get_cameras_as_json():
    try:
        cameras = Camera.query.all() 
        camera_list = []
        for camera in cameras:
            camera_data = {
                'id': camera.id,
                'name': camera.name,
                'location': camera.location,
                'video_type': camera.video_type,
                'video_link': camera.video_link,
                'frame_skip_size': camera.frame_skip_size,
                'address': camera.address,
                'lat': camera.lat,
                'long': camera.long, 
            }
            camera_list.append(camera_data)
            
        return jsonify(camera_list),200
    except Exception as e:
        return jsonify({"error": str(e)}),500

@camera_bp.route('/cameras/add', methods=["POST"])
def store_camera_config():
    print(request.get_json())
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    video_type = data.get('video_type')
    video_link = data.get('video_link')
    frame_skip_size = data.get('frame_skip_size')
    address = data.get('address')
    lat=data.get('lat')
    long=data.get('long')
     
    # Ensure that the JSON request contains the necessary fields
    if 'video_type' not in data or 'video_link' not in data:
        return jsonify({'message': 'Missing camera_id or config field in request'}), 400

    # Store the camera configuration in MongoDB
    try:
       
        camera=Camera(name=name,location=location,video_link=video_link,video_type=video_type,frame_skip_size=frame_skip_size,address=address,lat=lat,long=long)
        db.session.add(camera)
        db.session.commit()
        
        return jsonify({'message': 'Camera configuration stored successfully'}), 201
    except Exception as e:
        print(str(e))
        return jsonify({'message': str(e)}), 500


@camera_bp.route("/cameras/<string:camera_id>", methods=["GET"])
def get_camera_configuration(camera_id):
    print(camera_id)
    camera=Camera.query.get(camera_id)
    if camera is None:
        return jsonify({"error": "Camera not found"}), 404
    if camera:
        # Convert the Camera object to a dictionary
        camera_data = {
                'id': camera.id,
                'name': camera.name,
                'location': camera.location,
                'video_type': camera.video_type,
                'video_link': camera.video_link,
                'frame_skip_size': camera.frame_skip_size,
                'address': camera.address,
                'lat': camera.lat,
                'long': camera.long, 
            }
        
        return jsonify(camera_data), 200
    return "Camera not found", 404

@camera_bp.route('/cameras/update/<string:camera_id>', methods=['PUT'])
def edit_camera_configuration(camera_id):
    try:
        # Get data from the request JSON
        data = request.json
        camera = Camera.query.get(camera_id)
        
        if camera is None:
            return jsonify({"error": "Camera not found"}), 404

        updated_fields = data.get("updated_fields")
        print(updated_fields,camera_id)
        # Check if the camera ID and updated fields are provided
        if not updated_fields:
            print("no update fileds")
            return jsonify({"message": "Missing camera_id or updated_fields"}), 400
         
        for key, value in updated_fields.items():
            setattr(camera, key, value)
        
        db.session.commit()

        return jsonify({"message": "Camera configuration updated successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@camera_bp.route('/cameras/<string:camera_id>', methods=['DELETE'])
def delete_camera_configuration(camera_id):
    try:
        # Get data from the request JSON
        camera = Camera.query.get(camera_id)

        if camera is None:
            return jsonify({"error": "Camera not found"}), 404
        
        db.session.delete(camera)
        db.session.commit()
        return jsonify({"message": "Camera deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500