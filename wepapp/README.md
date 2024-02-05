# Weapon Detection Toolkit (Wep)

version 1.0

## Overview

This python-based toolkit uses trained AI models to report the existence of weapons in video-based content.

The following weapons can be detected
- Hand guns
- Rifles
- Knives

The following video technology can be processed
- mp4
- webm
- rtsp
- mjpeg

Weapon detection events can be optionally archived and published via the following technologies
- MQTT pub/sub
- Raptor API
- REST services

## Configuration

Wep configuration is defined within 5 stanzs
- Source - mp4 file name, rtsp stream URL, etc.
- Log config directives
- Processor directives
- Inference directives
- Publishing directives

The following represents a sample Wep configuration file

```js
[source]
  file_name = 9mm_fast_walk.mp4
  friendly_name = fast_walk
  building = Building A
  video_type = mp4
  video_link = /user/home/wep/videos/9mm_fast_walk.mp4
  #video_link = rtsp://admin:xxxx.interplay.iterate.ai/test1.sdp
  #video_link = rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4
  #video_link = rtsp://admin:xxxx@192.168.1.247
  stream_read_duration = 300

[log]
  log_config_file = weplog.conf

[processor]
  knife_threshold = 0.7
  output_path = /user/home/wep/inferences/
  bad_frame_skip_size = 10
  frame_skip_size = 100

[inference]
  framework = tf
  weights_weapon = /user/home/weaponresource/checkpoints_weapon/WeaponOct7_608_6000/
  input_size_weapon = 608
  tiny = False
  model = yolov4
  # output_format = XVID
  # for webm
  output_format = vp80
  iou_weapon = 0.5
  score_weapon = 0.3
  crop_rate = 150

[mqtt]
  enable = True
  broker = localhost
  topic = /wep/results
  user = none
  password = none

[raptor]
  enable = True
  url_token = https://staginglogin.raptortech.com/oauth/token
  url_building = https://api-stag.raptortech.com/clientbuilding/v1/Buildings
  url_template = https://api-stag.raptortech.com/incidents/v1/IncidentTemplate
  url_incident = https://api-stag.raptortech.com/incidents/v1/Incident/Create
  client_id = xxxx
  client_secret = yyyy
  audience = https://api-stag.raptortech.com
  grant_type = client_credentials
  client_token = zzzz
  buildingUID = aaaa
  templateUID = bbbb
  templateName = Lockdown
  lat = 29.806123
  long = -95.409467
  additionalData = Initiated by partner
  isDrill = false
```

## Invocation

Invcocation from a TTY can be done as follows. It will look for a file named `wep.ini` in the current dir for config info

```sh
$ python wep.py
```

A specific config file can be specified as a command argument as follows:

```sh
$ python wep.py my_wep_config.ini
```

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF

## Execution

The following is a sample run of the code with the following salient settings (see config info above for reference):
- data source type (video_type = mp4)
- data source path (video_link = /user/home/wep/videos/9mm_fast_walk.mp4)
- every 100th frame is analyzed (frame_skip_size = 100)
- results are written to `parent` directory (output_path = /user/home/wep/inferences/)
- results written to output dir under `output_path` (see above) called `fast_walk` (friendly_name = fast_walk)
- log level set to `info` (log_config_file = weplog.conf)
- results published to topic `/wep/results` (topic = /wep/results):

Note the detection event warning at timestampe `2023-03-07 14:37:41` and subsequent event publishing at `2023-03-07 14:37:43`.

```js
$ python wep.py 
2023-03-07 14:37:23 : INFO : <module> : 30 - Setup complete (v1.0)
2023-03-07 14:37:23 : INFO : <module> : 48 - Input request: {'video_link': '/user/home/wep/videos/9mm_fast_walk.mp4', 'building': 'Building A', 'video_type': 'mp4', 'friendly_name': 'fast_walker', 'file_original_name': '9mm_fast_walk.mp4'}
2023-03-07 14:37:23 : INFO : <module> : 59 - Detection for video starts...
2023-03-07 14:37:23 : INFO : <module> : 61 - GPU Utilization before: 
| ID | GPU | MEM |
------------------
2023-03-07 14:37:23.979069: I tensorflow/core/platform/cpu_feature_guard.cc:142] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
2023-03-07 14:37:23 : INFO : <module> : 23 - imported packages within inference_images_weapon
2023-03-07 14:37:23 : INFO : <module> : 41 - loading weapon model: tf
2023-03-07 14:37:37 : INFO : <module> : 50 - loaded weapon model
2023-03-07 14:37:37 : INFO : detect : 70 - msg_local_py[payload]: {'video_link': '/user/home/wep/videos/9mm_fast_walk.mp4', 'building': 'Building A', 'video_type': 'mp4', 'friendly_name': 'fast_walker', 'file_original_name': '9mm_fast_walk.mp4'}
2023-03-07 14:37:37 : INFO : detect : 136 - Begin video capture now: /user/home/wep/videos/9mm_fast_walk.mp4
2023-03-07 14:37:37 : INFO : detect : 141 - video: <VideoCapture 0x7fe43c747cd0>
2023-03-07 14:37:37 : WARNING : detect : 193 - fast_walker folder created
2023-03-07 14:37:38 : INFO : detect : 272 - Frame #: 100 of 258
2023-03-07 14:37:38 : INFO : inference_images_weapon : 57 - started weapon inference
2023-03-07 14:37:38.539267: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:185] None of the MLIR Optimization Passes are enabled (registered 2)
2023-03-07 14:37:39 : INFO : inference_images_weapon : 87 - fps after inference: 0.7183856574439417
2023-03-07 14:37:39 : INFO : inference_images_weapon : 145 - Ended weapon inference
2023-03-07 14:37:39 : INFO : detect : 280 - FPS01: 0.72
2023-03-07 14:37:39 : INFO : detect : 338 - After fetching img
2023-03-07 14:37:40 : INFO : detect : 416 - FPS02: 0.65
2023-03-07 14:37:41 : INFO : detect : 272 - Frame #: 200 of 258
2023-03-07 14:37:41 : INFO : inference_images_weapon : 57 - started weapon inference
2023-03-07 14:37:41 : INFO : inference_images_weapon : 87 - fps after inference: 1.59098129954861
2023-03-07 14:37:41 : INFO : inference_images_weapon : 145 - Ended weapon inference
2023-03-07 14:37:41 : INFO : detect : 280 - FPS01: 1.57
2023-03-07 14:37:41 : INFO : detect : 327 - After sending the input
2023-03-07 14:37:41 : INFO : detect : 338 - After fetching img
2023-03-07 14:37:41 : WARNING : detect : 376 - Gun : 0.8865709 Detected in Frame: 200
2023-03-07 14:37:41 : INFO : detect : 395 - output assignment. formatvp80 path:/user/home/wep/inferences/
OpenCV: FFMPEG: tag 0x30387076/'vp80' is not supported with codec id 139 and format 'webm / WebM'
2023-03-07 14:37:41 : INFO : detect : 416 - FPS02: 1.09
2023-03-07 14:37:43 : INFO : detect : 217 - Ended video inference here
2023-03-07 14:37:43 : INFO : <module> : 65 - Response: {'payload': [{'status': 'Completed', 'video_name': 'fast_walker', 'video_type': 'mp4', 'datetime': '07-03-2023 14:37:43', 'Threat_status': '', 'last_updated': True}]} <class 'dict'>
2023-03-07 14:37:43 : INFO : <module> : 67 - GPU Utilization after:
| ID | GPU | MEM |
------------------
2023-03-07 14:37:43 : INFO : do_mqtt : 23 - connecting to broker: localhost
2023-03-07 14:37:43 : INFO : do_mqtt : 26 - Publishing message to topic /wep/results
```

## Raptor

A tool name `raptor_tool.py` is provided to support the Raptor API as it has its own ecosystem. Note that it uses the same config file the `wep.py` app uses for config info, specifically, the `raptor` stanza. It's manifested in 4 phases:
- fetch auth token
- fetch building info
- fetch incident template
- create incident

The first three phases are performed from `raptor_tool.py` allowing the fourth phase to be done from `wep.py` app.

That is, artifacts from the tool are to be copied into the `raptor` config stanza (see above). Once done, results can be published when threats are detected.

A sample invocation follows:

```js
$ python raptor_tool.py
Input Raptor request: b[uilding] | t[emplate] | g[en token] c[reate incident]: 
```

The following shows a sample invocation which creates of a token:

```js
$ python raptor_tool.py <<< g
Input Raptor request: b[uilding] | t[emplate] | g[en token] c[reate incident]: Token info:
 {
  "access_token": "xxxx",
  "scope": "canmanageincidents read:buildings canperformreunificationtasks canmanageincidentstudents caninitiateincident",
  "expires_in": 86400,
  "token_type": "Bearer"
}
```

The following shows a sample invocation that displays building info:

```js
$ python raptor_tool.py <<< b
Input Raptor request: b[uilding] | t[emplate] | g[en token] c[reate incident]: Building info:
 [
  {
    "uid": "xxxx",
    "id": 7324,
    "clientId": 0,
    "clientUID": "zzzz",
    "name": "Place A",
    "addressLine1": "123 A Street",
    "addressLine2": null,
    "addressLine3": null,
    "city": "Some Town",
    "state": "California",
    "zip": "95128",
    "country": "US",
    "timeZoneId": 4,
    "createdDate": "2022-05-12T20:35:25.783+00:00"
  },
  {
    "uid": "yyyy",
    "id": 7325,
    "clientId": 0,
    "clientUID": "zzzz",
    "name": "Place B",
    "addressLine1": "123 B Street",
    "addressLine2": null,
    "addressLine3": null,
    "city": "Another Town",
    "state": "Colorado",
    "zip": "80123",
    "country": "US",
    "timeZoneId": 3,
    "createdDate": "2022-05-12T20:36:48.243+00:00"
  }
]
```

Similar is done for `incident template` data.

## Third party software
- Tensorflow library version 2.6.0 or later
- Paho MQTT library is used for MQTT client (pip install paho-mqtt)
- Standard logging library is used for logging
- GPUtil library used to show GPU utilization where pertinent

## License

MIT

## Authors

Balasundram Arunn, Chatura Samarasinghe, Reed McCauley

