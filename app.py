import sys
import signal
from flask import Flask, request, render_template
from flask_restful import Api, Resource
from threading import Thread
import multiprocessing as mp
import subprocess
from test.test import test_bp
import camera.camera as cameras
import event.event as events

app = Flask(__name__)
api = Api(app)

app.register_blueprint(test_bp, url_prefix='/test')
app.register_blueprint(cameras.camera_bp, url_prefix='/camera')
app.register_blueprint(events.event_bp, url_prefix='/event')

@app.route("/")
def home():
	return render_template("index.html")

def start_wep_instance(ini_file):
	try:
		result = subprocess.run(["./weprunner.sh", ini_file], shell=False, capture_output=True, text=True)
	except Exception as e:
		print("wep process ended")

wep_processes = []

def signal_handler(sig, frame):
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
	cameras.init()
	print(cameras.to_camera_ini_name(cameras.get_cameras()[0]))
	print(cameras.cameras_to_json())
	for camera in cameras.get_cameras():
		print(f"starting wep process for camera '{camera.name}'")
		wep_process = mp.Process(target=start_wep_instance, args=(cameras.to_camera_ini_name(camera),))
		wep_processes.append(wep_process)
		wep_process.start()
	print(events.events_to_json())
	events.init()
	for event in events.get_events():
		print(f"event status: {event.status}, video name: {event.video_name}, threat: {event.Threat_status}, path: {event.image_path}, images: {event.weapon_images[0]}")
	app.run()