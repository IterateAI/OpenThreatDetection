
#tf=""
model=""
data_all=""
import os
import time
import tensorflow as tf
from wepcore.functions import *
from absl import app, flags, logging
from absl.flags import FLAGS
import wepcore.utils as utils
from wepcore.yolov4 import filter_boxes
import GPUtil
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import logging as log
import wepcore.setup as cfg

log.info("imported packages within inference_images_weapon")

weights_weapon = cfg.weights_weapon
framework = cfg.framework
input_size_weapon = cfg.input_size_weapon
tiny = cfg.tiny
model = cfg.model
output_format = cfg.output_format
iou_weapon = cfg.iou_weapon
score_weapon = cfg.score_weapon

count= False
dont_show= False
info= False
crop= False
ocr= False
plate= False

log.info("loading weapon model: {}".format(framework))
if framework == 'tflite':
    interpreter = tf.lite.Interpreter(model_path=weights_weapon)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    log.info("loaded weapon model")
else:
    saved_model_loaded_weapon = tf.saved_model.load(weights_weapon, tags=[tag_constants.SERVING])
    log.info("loaded weapon model")

def inference_images_weapon(image_mask1,video_name,frame_num):
    log.debug("Input: {} {} {}".format(image_mask1, video_name, frame_num))
    try:
        
        #starttime0 = time.time()
        log.info("started weapon inference")
        image_data = cv2.resize(image_mask1, (input_size_weapon, input_size_weapon))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()    #detection starting time
        # print(start_time)    #o/p:1622462456.7511091
        # print('weapon image data',image_data)
        if framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            if model == 'yolov3' and tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size_weapon, input_size_weapon]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size_weapon, input_size_weapon]))
        else:
            infer_weapon = saved_model_loaded_weapon.signatures['serving_default']

            batch_data = tf.constant(image_data)
            pred_bbox = infer_weapon(batch_data) #inference happens hrer
            end_time = time.time()

            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        fps_01 = 1 / (time.time() - start_time )
        # time1 = (time.time() - start_time )
        log.info("fps after inference: {}".format(fps_01))

        # run non max suppression on detections
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=iou_weapon,
            score_threshold=score_weapon
        )
        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = image_mask1.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)

        # hold all detection data in one variable
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

        # rmm
        class_names = utils.read_class_names("./wepdata/classes/weapons.names")
        # print(class_names)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())
        #end_time3 = time.time()

        
        # if crop flag is enabled, crop each detection and save it as new image
        if crop:
            crop_rate = cfg.crop_rate # capture images every so many frames (ex. crop photos every 150 frames)
            crop_path = os.path.join(os.getcwd(), 'detections', 'crop', video_name)
            try:
                os.mkdir(crop_path)
            except FileExistsError:
                pass
            if frame_num % crop_rate == 0:
                final_path = os.path.join(crop_path, 'frame_' + str(frame_num))
                try:
                    os.mkdir(final_path)
                except FileExistsError:
                    pass
                crop_objects(cv2.cvtColor(image_mask1, cv2.COLOR_BGR2RGB), pred_bbox, final_path, allowed_classes)
            else:
                pass

        
        # if count flag is enabled, perform counting of objects
        if count:
            # count objects found
            counted_classes = count_objects(pred_bbox, by_class = False, allowed_classes=allowed_classes)
            # loop through dict and print
            for key, value in counted_classes.items():
                log.debug("Number of {}s: {}".format(key, value))
            image2 = utils.draw_bbox(image_mask1, pred_bbox, info, counted_classes, allowed_classes=allowed_classes, read_plate = plate)
        else:
            image2 = utils.draw_bbox(image_mask1, pred_bbox, info, allowed_classes=allowed_classes, read_plate = plate)

        log.info("Ended weapon inference")

    except Exception as e:
        log.error("Process exception occurred inside weapon inference: {}".format(e))
        pass


    return (image2,start_time,end_time,scores,classes)
