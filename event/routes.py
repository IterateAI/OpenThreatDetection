from flask import Blueprint, render_template, request, redirect, url_for,jsonify
import json
from .models import Event
from datetime import datetime
from extenstions import db

event_bp = Blueprint('event_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets')

@event_bp.route('/')
def home():
    events = Event.query.all() 
    return render_template("event/event.html", events=events)


@event_bp.route('/events', methods=["GET"])
def get_events_as_json():
    try:
        events = Event.query.all() 
        event_list=[]
        for event in events:
            event_data=event.as_dict()
            event_list.append(event_data)
        
        return jsonify(event_list),200
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@event_bp.route('/events', methods=["POST"])
def add_event_as_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        dataJson=json.loads(data)
        print("Data type",type(json.loads(data)))
        print("Data ",json.loads(data))

        if 'status' not in data or 'video_name' not in data:
            return jsonify({'message': 'Missing camera_id or config field in request'}), 400
        try:
            status=dataJson.get('status')
            video_name=dataJson.get('video_name')
            date_time=dataJson.get('datetime')
            Threat_status=dataJson.get('Threat_status')
            image_path=dataJson.get('image_path')
            weapon_images=dataJson.get('weapon_images')[0]
            timestamp=datetime.now()
            event=Event(status=status,video_name=video_name,date_time=date_time,Threat_status=Threat_status,image_path=image_path,weapon_images=weapon_images,timestamp=timestamp)
            db.session.add(event)
            db.session.commit()
            return jsonify({'message': 'Event stored successfully'}), 201
        except Exception as e:
            print(str(e))
            return jsonify({'message': str(e)}), 500
    else:
        print("Unsupported content type: " + content_type)
        return 'Content-Type not supported!', 500
    
@event_bp.route("/events/<string:event_id>", methods=["GET"])
def get_camera_configuration(event_id):
    print(event_id)
    alerts = Event.query.get(event_id)
    if alerts is None:
        return jsonify({"error": "Camera not found"}), 404
    if alerts:
        event_data =alerts.as_dict()
        return jsonify(event_data), 200
    return "Camera not found", 404  