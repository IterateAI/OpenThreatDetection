import sys
import signal
from flask import Flask, request, render_template,send_from_directory
from flask_restful import Api, Resource
from threading import Thread
import multiprocessing as mp
import subprocess
from test.test import test_bp
from camera.routes import camera_bp
from event.routes import event_bp

from extenstions import db

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(app)
app.register_blueprint(test_bp, url_prefix='/api/test')
app.register_blueprint(camera_bp, url_prefix='/api/camera')
app.register_blueprint(event_bp, url_prefix='/api/event')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weapon.db'  # SQLite database file
db.init_app(app)

from camera import models
with app.app_context():
	db.create_all()

app.debug=True

@app.route("/api")
def home():	
	return render_template("index.html")

@app.route("/public/<path:filename>")
def serve_file(filename):
	print("FIles",filename)
	return send_from_directory('./wepapp/inferences',filename)


def start_wep_instance(ini_file):
	try:
		result = subprocess.run(["./weprunner.sh", ini_file], check=True, shell=False, capture_output=True, text=True )
		# print("subprocess",result)
	except Exception as e:
		print("wep process ended",e)
  
def start_webhook():
	try:
		result = subprocess.run(["./web_hook.sh"],shell=False, capture_output=True, text=True)
	except Exception as e:
		print("wep process ended")

wep_processes = []

web_hooks = []

def signal_handler(sig, frame):
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

from  camera import camera as cameras
import event.event as events
if __name__ == "__main__":
    
	cameras.init()
	# print(cameras.to_camera_ini_name(cameras.get_cameras()[0]))
	# print(cameras.cameras_to_json())
	for camera in cameras.get_cameras():
		print(f"starting wep process for camera '{camera.name}'")
		wep_process = mp.Process(target=start_wep_instance, args=(cameras.to_camera_ini_name(camera),))
		wep_processes.append(wep_process)
		wep_process.start()
	web_hook = mp.Process(target=start_webhook, args=())
	web_hooks.append(web_hook)
	web_hook.start()
	print(events.events_to_json())
	events.init()
	for event in events.get_events():
		print(f"event status: {event.status}, video name: {event.video_name}, threat: {event.Threat_status}, path: {event.image_path}, images: {event.weapon_images[0]}")
	app.run()