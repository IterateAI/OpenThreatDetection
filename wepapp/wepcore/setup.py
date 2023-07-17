
from configparser import ConfigParser
from pathlib import Path
import logging.config
import logging as log
import wepcore.constants as cons
import sys
import typing

if __name__ == 'wepcore.setup':

	version_info = 'v1.0'
	
	is_valid = False
	config_file = "wep.ini"
	if len(sys.argv) > 1:
		config_file = sys.argv[1];

	try:
		if not Path(config_file).is_file():
			raise FileNotFoundError(config_file)
		config = ConfigParser()
		config.read(config_file)

		config.get(cons.SOURCE, cons.VIDEO_TYPE)
		config.get(cons.SOURCE, cons.FRIENDLY_NAME)
		config.get(cons.SOURCE, cons.BUILDING)
		config.get(cons.SOURCE, cons.VIDEO_LINK)

		source = config[cons.SOURCE]
		source.get(cons.VIDEO_TYPE)
		if not source.get(cons.VIDEO_TYPE) in cons.VIDEO_TYPES:
			raise TypeError("Invalid video type: {}, valid types: {}".format(source.get(cons.VIDEO_TYPE), cons.VIDEO_TYPES))

		if source.get(cons.VIDEO_TYPE) in cons.VIDEO_FILE_TYPES:
			if not Path(source.get(cons.VIDEO_LINK)).is_file():
				raise FileNotFoundError(source.get(cons.VIDEO_LINK))

		logc = config[cons.LOG]
		if not Path(logc.get(cons.LOG_CONFIG_FILE)).is_file():
			raise FileNotFoundError(logc.get(cons.LOG_CONFIG_FILE))
		log.config.fileConfig(logc.get(cons.LOG_CONFIG_FILE))

		config.get(cons.PROCESSOR, cons.KNIFE_THRESHOLD)
		config.get(cons.PROCESSOR, cons.OUTPUT_PATH)
		config.get(cons.PROCESSOR, cons.BAD_FRAME_SKIP_SIZE)
		config.get(cons.PROCESSOR, cons.FRAME_SKIP_SIZE)
		processor = config[cons.PROCESSOR]
		knife_threshold = float(processor.get(cons.KNIFE_THRESHOLD))
		output_path = processor.get(cons.OUTPUT_PATH)
		if output_path == "False":
			output_path = False
		bad_frame_skip_size = int(processor.get(cons.BAD_FRAME_SKIP_SIZE))
		frame_skip_size = int(processor.get(cons.FRAME_SKIP_SIZE))
		log.debug("Proc info: {}".format({
			cons.KNIFE_THRESHOLD: knife_threshold,
			cons.OUTPUT_PATH: output_path,
			cons.BAD_FRAME_SKIP_SIZE: bad_frame_skip_size,
			cons.FRAME_SKIP_SIZE: frame_skip_size}))

		inference = config[cons.INFERENCE]
		config.get(cons.INFERENCE, cons.FRAMEWORK)
		config.get(cons.INFERENCE, cons.WEIGHTS_WEAPON)
		config.get(cons.INFERENCE, cons.INPUT_SIZE_WEAPON)
		config.get(cons.INFERENCE, cons.TINY)
		config.get(cons.INFERENCE, cons.MODEL)
		config.get(cons.INFERENCE, cons.OUTPUT_FORMAT)
		config.get(cons.INFERENCE, cons.IOU_WEAPON)
		config.get(cons.INFERENCE, cons.SCORE_WEAPON)
		config.get(cons.INFERENCE, cons.CROP_RATE)
		framework = inference.get(cons.FRAMEWORK)
		weights_weapon = inference.get(cons.WEIGHTS_WEAPON)
		input_size_weapon = int(inference.get(cons.INPUT_SIZE_WEAPON))
		tiny = inference.get(cons.TINY)
		if tiny == "False":
			tiny = False
		model = inference.get(cons.MODEL)
		output_format = inference.get(cons.OUTPUT_FORMAT)
		iou_weapon = float(inference.get(cons.IOU_WEAPON))
		score_weapon = float(inference.get(cons.SCORE_WEAPON))
		crop_rate = int(inference.get(cons.CROP_RATE))
		stream_read_duration = cons.STREAM_READ_DURATION_DEFAULT
		try:
			config.get(cons.SOURCE, cons.STREAM_READ_DURATION)
			stream_read_duration = int(source.get(cons.STREAM_READ_DURATION))
		except ValueError as v:
			log.warn("Invalid stream_read_duration config value '{}', using default: {}"
				.format(source.get(cons.STREAM_READ_DURATION), cons.STREAM_READ_DURATION_DEFAULT))
		except Exception as e:
			pass # default will be used
		log.debug("Inference info: {}".format({
			cons.FRAMEWORK: framework,
			cons.WEIGHTS_WEAPON: weights_weapon,
			cons.INPUT_SIZE_WEAPON: input_size_weapon,
			cons.TINY: tiny,
			cons.MODEL: model,
			cons.OUTPUT_FORMAT: output_format,
			cons.IOU_WEAPON: iou_weapon,
			cons.SCORE_WEAPON: score_weapon,
			cons.CROP_RATE: crop_rate}))

		value = config.get(cons.MQTT, cons.ENABLE)
		if value.lower() != 'true' and value.lower() != 'false':
			raise ValueError('{} {} flag is invalid: {}'.format(cons.MQTT, cons.ENABLE, value))
		config.get(cons.MQTT, cons.BROKER)
		config.get(cons.MQTT, cons.TOPIC)
		mqtt: typing.Dict[str,object] = {
			cons.ENABLE: True if value.lower() == 'true' else False,
			cons.BROKER: config.get(cons.MQTT, cons.BROKER),
			cons.TOPIC: config.get(cons.MQTT, cons.TOPIC)
		}
		log.debug("MQTT info: {}".format(mqtt))

		while True:
			value = config.get(cons.RAPTOR, cons.ENABLE)
			if value.lower() != 'true' and value.lower() != 'false':
				raise ValueError('{} {} flag is invalid: {}'.format(cons.RAPTOR, cons.ENABLE, value))
			if value.lower() == 'false':
				raptor: typing.Dict[str,object] = {
					cons.ENABLE: False
				}
				break
			config.get(cons.RAPTOR, cons.CLIENT_TOKEN)
			config.get(cons.RAPTOR, cons.BUILDING_UID)
			config.get(cons.RAPTOR, cons.TEMPLATE_UID)
			config.get(cons.RAPTOR, cons.TEMPLATE_NAME)
			config.get(cons.RAPTOR, cons.LATITUDE)
			config.get(cons.RAPTOR, cons.LONGITUDE)
			config.get(cons.RAPTOR, cons.ADDITIONAL_DATA)
			value = config.get(cons.RAPTOR, cons.IS_DRILL)
			config.get(cons.RAPTOR, cons.CLIENT_ID)
			config.get(cons.RAPTOR, cons.CLIENT_SECRET)
			config.get(cons.RAPTOR, cons.AUDIENCE)
			config.get(cons.RAPTOR, cons.GRANT_TYPE)
			config.get(cons.RAPTOR, cons.URL_TOKEN)
			config.get(cons.RAPTOR, cons.URL_BUILDING)
			config.get(cons.RAPTOR, cons.URL_TEMPLATE)
			config.get(cons.RAPTOR, cons.URL_INCIDENT)
			latitude = float(config.get(cons.RAPTOR, cons.LATITUDE))
			longitude = float(config.get(cons.RAPTOR, cons.LONGITUDE))
			if value.lower() != 'true' and value.lower() != 'false':
				raise ValueError('{} {} flag is invalid: {}'.format(cons.RAPTOR, cons.IS_DRILL, value))
			raptor = {
				cons.ENABLE: True,
				cons.CLIENT_TOKEN: config.get(cons.RAPTOR, cons.CLIENT_TOKEN),
				cons.BUILDING_UID: config.get(cons.RAPTOR, cons.BUILDING_UID),
				cons.TEMPLATE_UID: config.get(cons.RAPTOR, cons.TEMPLATE_UID),
				cons.TEMPLATE_NAME: config.get(cons.RAPTOR, cons.TEMPLATE_NAME),
				cons.LATITUDE: config.get(cons.RAPTOR, cons.LATITUDE),
				cons.LONGITUDE: config.get(cons.RAPTOR, cons.LONGITUDE),
				cons.ADDITIONAL_DATA: config.get(cons.RAPTOR, cons.ADDITIONAL_DATA),
				cons.IS_DRILL: True if value.lower() == 'true' else False,
				cons.CLIENT_ID: config.get(cons.RAPTOR, cons.CLIENT_ID),
				cons.CLIENT_SECRET: config.get(cons.RAPTOR, cons.CLIENT_SECRET),
				cons.AUDIENCE: config.get(cons.RAPTOR, cons.AUDIENCE),
				cons.GRANT_TYPE: config.get(cons.RAPTOR, cons.GRANT_TYPE),
				cons.URL_TOKEN: config.get(cons.RAPTOR, cons.URL_TOKEN),
				cons.URL_BUILDING: config.get(cons.RAPTOR, cons.URL_BUILDING),
				cons.URL_TEMPLATE: config.get(cons.RAPTOR, cons.URL_TEMPLATE),
				cons.URL_INCIDENT: config.get(cons.RAPTOR, cons.URL_INCIDENT)
			}
			log.debug("RAPTOR info: {}".format(raptor))

			value = config.get(cons.RESTFUL, cons.ENABLE)
			if value.lower() != 'true' and value.lower() != 'false':
				raise ValueError('{} {} flag is invalid: {}'.format(cons.RESTFUL, cons.ENABLE, value))
			config.get(cons.RESTFUL, cons.URL)
			restful: typing.Dict[str,object] = {
				cons.ENABLE: True if value.lower() == 'true' else False,
				cons.URL: config.get(cons.RESTFUL, cons.URL),
			}
			log.debug("RESTful info: {}".format(restful))
			break
	except FileNotFoundError as f:
		log.error('File does not exist: {}'.format(f))
	except Exception as e:
		log.error('General Error: {}'.format(e))
	else:
		is_valid = True

	if not is_valid:
		exit()


