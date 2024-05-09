import logging as log
import paho.mqtt.client as mqtt
import urllib3
import json
import wepcore.setup as cfg
import wepcore.constants as cons
import requests

http = urllib3.PoolManager()

local_restful_event_url = "http://127.0.0.1:5000/api/event/events"

def do_push(data_weapon):
	# do_mqtt(data_weapon)
	# do_raptor_create_incident(data_weapon)
	do_restful(data_weapon)

def do_restful(data_weapon):
	try:
		log.info("RESTful: {}".format(cfg.restful))
		if not cfg.restful[cons.ENABLE]:
			log.info("RESTful post is disabled")
			return

		log.info("post to local wep RESTful service " + data_weapon)
		response = requests.post(local_restful_event_url, json=data_weapon)
		log.info(f"response: {response}")

		log.info("post to remote RESTful service " + data_weapon + ", url:" + cfg.restful[cons.URL])
		response = requests.post(cfg.restful[cons.URL], json=data_weapon)
		log.info(f"response: {response}")
	except Exception as e:
		log.error("Failed to post to RESTful service: {}".format(e))
	pass

def do_mqtt(data_weapon):
	try:
		log.debug("MQTT: {}".format(cfg.mqtt))
		if not cfg.mqtt[cons.ENABLE]:
			log.info("MQTT is disabled")
			return

		client = mqtt.Client()

		log.info("connecting to broker: {}".format(cfg.mqtt[cons.BROKER]))
		client.connect(cfg.mqtt[cons.BROKER])

		log.info("Publishing message to topic {}".format(cfg.mqtt[cons.TOPIC]))
		client.publish(cfg.mqtt[cons.TOPIC],data_weapon)
	except Exception as e:
		log.error("Failed to publish to MQTT service: {}".format(e))
	pass


def raptor_get_token():
	try:
		log.debug("Raptor: {}".format(cfg.raptor))
		if not cfg.raptor[cons.ENABLE]:
			log.info("Raptor is disabled")
			return

		data = {cons.CLIENT_ID: cfg.raptor[cons.CLIENT_ID],
				cons.CLIENT_SECRET: cfg.raptor[cons.CLIENT_SECRET],
				cons.AUDIENCE: cfg.raptor[cons.AUDIENCE], 
				cons.GRANT_TYPE: cfg.raptor[cons.GRANT_TYPE]
				}
		edata = json.dumps(data).encode('utf-8')
		log.debug(edata)
		r = http.request(
			'POST',
		    cfg.raptor[cons.URL_TOKEN],
			headers={'content-type': 'application/json'},
		    body=edata
	    )

		if r.status != 200:
			raise RuntimeError(r.data)
		print("Token info:\n",json.dumps(json.loads(r.data), indent=2))
	except Exception as e:
		log.error("Failed to process Raptor client token fetch request: {}".format(e))
	pass

def raptor_building_info():
	try:
		log.debug("Raptor: {}".format(cfg.raptor))
		if not cfg.raptor[cons.ENABLE]:
			log.info("Raptor is disabled")
			return
			
		r = http.request(
		    'GET',
		    cfg.raptor[cons.URL_BUILDING],
		    headers={"Authorization":"Bearer " + cfg.raptor[cons.CLIENT_TOKEN], "content-type":"application/json"}
	    )
		print("Building info:\n",json.dumps(json.loads(r.data), indent=2))
	except Exception as e:
		log.error("Failed to process Raptor building fetch request: {}".format(e))
	pass