### Prerequisites

- The system must be Linux-based and support GPU for running the backend.
- For running on a Windows PC, set up WSL: [WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install).

### Clone Repository with Large Files

1. **Open Terminal** (For Windows, open WSL Ubuntu Terminal):

    ```sh
    # Install git-lfs to download large files from GitHub
    sudo apt-get install git-lfs
    git lfs install
    
    # Clone the repository
    git clone https://github.com/IterateAI/OpenThreatDetection.git
    ```

2. **Change Directory**:

    ```sh
    cd OpenThreatDetection
    ```

3. **Install Python 3.10** (if not already installed):

    ```sh
    sudo apt install python3.10-venv
    ```

4. **Change Ownership of the Directory** (Replace `<user>` with your username):

    ```sh
    sudo chown -R $(whoami) /home/<user>/OpenThreatDetection
    ```

### Weapon Detection Startup/Shutdown

**Startup:**

1. Navigate to the project directory:

    ```sh
    cd /home/<user>/OpenThreatDetection
    ```

2. Activate the virtual environment (assuming it has been set up):

    ```sh
    source venv/bin/activate
    ```
3. Install required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Start the backend service (assuming a specific command or script is provided):

    ```sh
    python3 app.py
    ```
WEPWEB is started from a TTY and binds to port 5000 as follows.

4. Deactivate the virtual environment(Optional)

    ```sh
    deactivate
    ```

# Frontend

![Alt text](image.png)
![Alt text](image-1.png)
## Running the Next.js Frontend
Open Another terminal for Frontend and follow the below stpes. (WSL Ubuntu terminal for Windows pc)

### Prerequisites
Make sure you have the following installed on your machine:

- Node.js: Download and Install Node.js v20
- npm (Node Package Manager): npm is included with Node.js installation.

### Steps
```js
cd /home/<user>/OpenThreatDetection/frontend
```

```js
npm install
npm run dev
```
Open your web browser and navigate to http://localhost:3000. You should see your Next.js application running.
### Troubleshooting
If you encounter issues, refer to the Next.js documentation(https://nextjs.org/docs) for troubleshooting and additional information.


# Weapon Detection Web Application (WEPWEB)

version 1.0


## Glossary
WDE - Weapon Dedection Event
WEPAPP - Toolkit that uses trained AI models to report the existence of WDEs when dedected via streaming devices, e.g., cameras
WEPWEB - Web kit that uses the Weapon Detection Application (WEPAPP) to collect, render and push HTTP-based WDEs
WEPHOOK - Webhook that registers for and renders WDEs in realtime

## Overview

This python-based Web kit uses the Weapon Detection Application (WEPAPP) to collect, render and push HTTP-based Weapon Detection events. See the webapp/README.md file for more information on the Wepapp toolkit

### WEPWEB is a Flask application built using Blueprint modules to support:
- Cameras
- Weapon Dedection Events

### Configuration files are found in the *config* directory:
- wep_ini_template.txt - used to create configuration files used by Web app instances, one for each camera
- weplog_template.txt - used to create log files used by Web app instances, one for each camera

### Carmera module
Cameras, along with WEPAPP software, scan for WDEs. The Camera module provides the following:
- processes/vets camera configuration data
- associates each configured camera with a separate, dedicated instance of WEPAPP

Processing steps:
- cameras.json is parsed to discover camera information
- for each camera, a WEPAPP init file is created using the wep_ini_template.txt file
- for each camera, a WEPAPP log file is created using the weplog_template.txt file
- for each camera, an instance (separate process) of WEPAPP is created using the corresponding init and log file

Cameras are configured with the following attributes:
- name - unqiue name, e.g., Science
- location - descriptive link, e.g., Science building"
- link_type - RTSP
- link - the RTSP camera link, formatted as: rtsp://username:password@camera-ip
- frame_skip_size - number of frames skipped before a frame is processed. Larger values provide better performance. Smaller values provide better accuracy.
- address - location address
- lat - latitude of location
- long - longitude of location

Camera configuration example. In the following, 3 cameras are defined for the Science, Library and Residence Hall locations, respectively:
```js
[
  {
  "name": "Science",
   "location": "Science Building",
   "video_type": "rtsp",
   "video_link": "rtsp://admin:pwd@192.168.1.247",
   "frame_skip_size": 100,
   "address": {"street": "1234 Science Way"},
   "lat": 12.345,
   "long": 45.56
  },
 ]

```

At WEPWEB startup, the Camera module will generate the following six files based on the above:
- wep_Science.ini
- weplog_Science.conf
- wep_Library.ini
- weplog_Library.conf
- wep_Residence.ini
- weplog_Residence.conf

Afterwhich, three WEPAPP processes will be started using the above sets of files. Each WEPAPP instance will monitor the RTSP link provided in their corresponding configuration files.

> See the WEPAPP README file for more details on configuration file content

### WDE module
The WDE module parses the events.json file to create a class object to hold detection event intel provided by the AI software. It contains the following metrics:
- status - what was detected and what is the accuracy score
- video_name - the name of the camera that recorded the event
- datetime - the date & time the event occurred
- image_path - a path to image of the detected weapon

A sample WEPAPP event json snippet follows:
```js
{'status': 'Weapon Detected |Gun : 0.87357223', 'video_name': 'Science', 'datetime': '30-06-2023 14:38:44', 'image_path': 'weapon_30-06-2023 14:38:44.jpg'}
```

### Database

The application uses SQLite as the database for storing and managing data. SQLite is a lightweight, serverless, and self-contained database engine, making it suitable for smaller applications and projects.

#### Setup

1. **Database File:**
   The SQLite database file is included in the project, typically named `weapon.db`. You don't need to set up a separate database server.

2. **Schema:**
   The database schema and structure can be found in the SQL scripts located in the `instance` directory. If there are migrations or initialization scripts, provide details on how to run them.
   
2. **Tables:**
- camera - store all the cameras configurations where events are detected
- event - store all the alerts and details in the format of weapon detections events

#### Connecting to the Database

- **Connection in Code:**
  In your application code, you can connect to the SQLite database using a library or ORM compatible with SQLite. Ensure that the necessary configurations, such as the database file path, are correctly set.

  ```python
  import sqlite3

  # Connect to the SQLite database
  connection = sqlite3.connect('path/to/database.db')


This will start a master process to oversee camera specific WEBAPP processes discussed below, e.g.:
```js
501 10662   574   0  7:29PM ttys002    0:00.34 python app.py
```
For the following example, assume the following camera configuration:

```js
  "cameras": [
    {"name": "Science", "location": "science", "link_type": "rtsp", "link": "rtsp://admin:iterate411@192.168.1.247", "frame_skip_size": 100, "address": {"street": "1234 Hargrave Way"}, "lat": -12.345, "long": 45.56},
    {"name": "Residence", "location": "residence", "link_type": "rtsp", "link": "rtsp://admin:iterate411@192.168.1.247", "frame_skip_size": 100, "address": {"street": "1234 Hargrave Way"}, "lat": -12.345, "long": 45.56}
  ]
}
```

Upon execution, the following files are generated by the Camera module and place in the config directory:
- wep_Residence.ini
- wep_Science.ini
- weplog_Residence.conf
- weplog_Science.conf

And the following WEPAPP processes are started using the above configuration files:
```js
  501 10670 10666   0  7:29PM ttys002    0:00.00 /bin/sh ./weprunner.sh config/wep_Residence.ini
  501 10671 10665   0  7:29PM ttys002    0:00.00 /bin/sh ./weprunner.sh config/wep_Science.ini
```

The log files for each camera are maintained in the logs directory. For example, for the above, the following files now exist with camera details logged to corresponding log files:
```js
-rw-r--r--  1 reed  staff  62605 Jul  3 19:41 wep_Science.log
-rw-r--r--  1 reed  staff  62630 Jul  3 19:41 wep_Residence.log
```

Startup data and event processing is logged to these files, for example:
```js
2023-07-03 19:29:42 : INFO : <module> : 30 - Setup complete (v1.0)
2023-07-03 19:29:42 : INFO : <module> : 39 - No GPU devices found
2023-07-03 19:29:42 : INFO : <module> : 50 - Input request: {'video_link': 'rtsp://admin:iterate411@192.168.1.247', 'building': 'science', 'video_type': 'rtsp', 'friendly_name': 'Science', 'file_original_name': None}
2023-07-03 19:29:42 : INFO : <module> : 58 - Detection for video stream starts...
2023-07-03 19:29:42 : INFO : <module> : 62 - GPU Utilization before: 
2023-07-03 19:29:42 : INFO : <module> : 23 - imported packages within inference_images_weapon
2023-07-03 19:29:42 : INFO : <module> : 41 - loading weapon model: tf
2023-07-03 19:29:58 : INFO : <module> : 50 - loaded weapon model
2023-07-03 19:29:58 : INFO : detect : 50 - Video source: rtsp://admin:iterate411@192.168.1.247
2023-07-03 19:29:58 : INFO : detect : 71 - msg_local_py[payload]: {'video_link': 'rtsp://admin:iterate411@192.168.1.247', 'building': 'science', 'video_type': 'rtsp', 'friendly_name': 'Science', 'file_original_name': None}
```

> See the WEPAPP README file for more details

To shutdown WEPWEB, send SIGINT (CTRL+C) or SIGTERM to the master WEPWEB process, e.g.,
```js
501 10662   574   0  7:29PM ttys002    0:00.34 python app.py
```

## Runtime and WDEs
As WDEs occur, the corresponding WEPAPP process will record the event to it's log file, e.g.:
```js
2023-07-03 19:51:47 : INFO : do_restful : 25 - post to local wep RESTful service {"status": "Weapon Detected |Gun : 0.94016784", "video_name": "Residence", "datetime": "03-07-2023 19:51:47", "Threat_status": "Threat detected | Weapon:['Gun : 0.94016784']", "image_path": "weapon_03-07-2023 19:51:47.jpg", "weapon_images": ["weapon_03-07-2023 19:51:47.jpg"]}
2023-07-03 19:51:47 : INFO : do_restful : 27 - response: <Response [200]>
2023-07-03 19:51:47 : INFO : do_restful : 29 - post to remote RESTful service {"status": "Weapon Detected |Gun : 0.94016784", "video_name": "Residence", "datetime": "03-07-2023 19:51:47", "Threat_status": "Threat detected | Weapon:['Gun : 0.94016784']", "image_path": "weapon_03-07-2023 19:51:47.jpg", "weapon_images": ["weapon_03-07-2023 19:51:47.jpg"]}, url:http://localhost:5001/consumeevent
```

> Note the message POST. WDE details are POSTed to a RESTful service configured for the WEPAPP instance. See the WEPAPP README for more details.
> In this case, it's posting the event to the WEAPP, for example:
```js
event_json type: <class 'dict'>
event_json: {'status': 'Weapon Detected |Gun : 0.94016784', 'video_name': 'Residence', 'datetime': '03-07-2023 19:51:47', 'Threat_status': "Threat detected | Weapon:['Gun : 0.94016784']", 'image_path': 'weapon_03-07-2023 19:51:47.jpg', 'weapon_images': ['weapon_03-07-2023 19:51:47.jpg']}
```

The WDE is recorded in the WEPWEB WDE list, it contains WDEs for all cameras.

## Webhook
The WEBAPP also configures an external RESTful service (binds to port 5001) to send WDEs to - it represents a Webhook. In our case, the WEBAPP config template specifies the following Webhook client URL:
```js
[restful]
  enable = True
  url = http://localhost:5001/consumeevent
```
> See WEBAPP README for more details

A WEPWEB Webhook is provided, implementing the consumeevent address mentioned above. The code is in the webhook_sample directory, embody in the following two files:
- webhook_consumer.py
- templates/webhook_consumer.html

The Webhook consumer is a standalone Flask app that runs on a separate port form WEPWEB. A sample startup session follows:
```js
$ python webhook_consumer.py 
Server initialized for eventlet.
 * Restarting with watchdog (fsevents)
Server initialized for eventlet.
 * Debugger is active!
 * Debugger PIN: 143-180-938
(11317) wsgi starting up on http://[::1]:5001
```

Subsequently, when the webhook_consumer.html is accessed from Web browser, WDEs will be streamed in realtime.

## Web pages
The following shows snippets of web pages described above.

### WEPWEB home page shows links to configured Cameras and any WDEs.

Selecting the Cameras tab will show configured camera info:
- Name
- Location of camera
- RTSP camera link

Selecting the Events tab will show any WDEs, one per line:
- Camera WDE occurred on
- Weapon type dedected and accuracy quotient
- Name of image capturing showing weapon

### WEPHOOK home page will register with the configured Webhook (see Webhook section above for more details) and stream any dedected WDEs by the WEPWEB app.
Each WDE will provide the following info:
- Camera WDE occurred on
- Weapon type dedected and accuracy percentage
- Name of image capturing showing weapon

The following is a sample WDE rendered by the WEPHOOK
* Science * 07-07-2023 11:28:26 * Weapon Detected |Gun : 82%  * weapon_07-07-2023 11:28:26.jpg

## Third party software
- Tensorflow library version 2.6.0 or later
- Paho MQTT library is used for MQTT client (optional - pip install paho-mqtt)
- Standard logging library is used for logging
- GPUtil library used to show GPU utilization where pertinent
- Flask
- Flask-RESTful
- Flask-SocketIO

## License

MIT

## Authors

Balasundram Arunn, Chatura Samarasinghe, Reed McCauley, Janarthan J, Gamsan Vigneswaran, Ramakrishnan Velmakivan

