from logging import exception	
from platform import python_version
import sys
import os
import json
import re
import pandas as pd
from datetime import datetime
import threading
import queue
import functools
import trace
import time
import GPUtil
import base64
import io
from PIL import Image
import tensorflow as tf
from wepcore.functions import *
from PIL import Image
import cv2
import numpy as np
import logging as log
import wepcore.constants as cons
import wepcore.setup as cfg
import wepcore.downstream_services as push

physical_devices = tf.config.experimental.list_physical_devices('GPU')

#this is to allocate memory for GPU usage for each process
if physical_devices:
  # Create 2 virtual GPUs with 1GB memory each
  try:
    tf.config.set_logical_device_configuration(
        physical_devices[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=1024*1),
         tf.config.LogicalDeviceConfiguration(memory_limit=1024*1)])
    logical_gpus = tf.config.list_logical_devices('GPU')
    log.info(len(physical_devices), "Physical GPU,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    log.error("GPU info fetch failed: {}".format(e))


def detect(msg_py,msg_local_py,msg_passing):
        from wepcore.inference_images_weapon import inference_images_weapon
        from tensorflow.compat.v1 import ConfigProto
        from tensorflow.compat.v1 import InteractiveSession

        log.info("Video source: {}".format(cfg.source.get(cons.VIDEO_LINK)))
        knife_threshold = cfg.knife_threshold # 0.7
        output_path_set = False

        config = ConfigProto()

        session = InteractiveSession(config=config)
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        weapon_arr = [] # append in json
        mask_arr = []  #append in json
        frame_sum_arr = []
        frame_sum_arr_except = []
        frames_arr = []
        exception_pro = ''
        completed_pro = ''
        current_pro = ''

        if msg_local_py is None:
            log.warn("msg_local_py none")
        elif msg_local_py is not None:
            ui=msg_local_py["payload"]
            log.info("msg_local_py[payload]: {}".format(ui))

            video_link = ui["video_link"]
            log.debug('video URL: {}'.format(video_link))

            building = ui["building"]
            log.debug('building: {}'.format(building))

            video_ext = ui["video_type"]
            log.debug('video Type: {}'.format(video_ext))

            video_friendly_name = ui["friendly_name"]
            log.debug('Friendly name: {}'.format(video_friendly_name))

            #video_original_name = ui["file_original_name"]
            #log.debug('Original name: {}'.format(video_original_name))

            video_name1 = video_friendly_name  #if needed add the extension
            video_name = video_friendly_name

            #when video url or friendly name is empty should add that to exception
            if ((video_ext=='rtsp') or (video_ext=='mjpeg')) and ((video_link =="") or (video_friendly_name=="")):  #validation
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                data1 = {'status':"Video link or friendly name is blank.",'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':"",'last_updated':True}

                log.error('Exception in the current frame: {}'.format(data1))
                frame_sum_arr_except.append(data1)
                msg_py['payload'] = frame_sum_arr_except    # this will be displayed in fronted using socket
                msg_passing.append(msg_py)

                return msg_py

                
            #when video url or friendly name is empty should add that to exception
            if ((video_ext=='mp4') or (video_ext=='webm')) and (video_friendly_name==""):  #validation
                log.info("Within the multiprocessing python within validating")
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                data1 = {'status':"Friendly name is blank.",'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':"",'last_updated':True}

                log.error('Exception in the current frame: {}'.format(data1))
                frame_sum_arr_except.append(data1)
                msg_py['payload'] = frame_sum_arr_except    # this will be displayed in fronted
                msg_passing.append(msg_py)

                return msg_py
            #######BEGIN INFERENCE



            #For videos, inference and save full video. 
            if (video_ext in ['mp4','webm']):
                video_path = video_link

            elif (video_ext in ['rtsp','mjpeg']):
                video_path = video_link
                stream_read_stop_time = 0
                if cfg.stream_read_duration > 0:
                    stream_read_stop_time = int(time.time()) + cfg.stream_read_duration



            log.info('Begin video capture now: {}'.format(video_path))
            if (video_ext in ['mp4','webm']):
                try:
                    vid = cv2.VideoCapture(str(video_path))
                    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
                    log.info("video: {}".format(vid))
                except Exception as e:
                    log.error('Video Capture Exception: {}'.format(e))
                    return msg_py
            elif (video_ext in ['rtsp','mjpeg']):
                try:
                    log.info("Within reading path")
                    vid = cv2.VideoCapture(str(video_path))  #to get height, width of the frame to save
                    vid_latest_rtsp = cv2.VideoCapture(video_path)    #Read the latest frame from rtsp stream
                    #########This part is added for find whether the rtsp stream url is invalid
                    return_value, frame = vid.read()

                    if not return_value:
                        log.error("Stream URL is invalid")

                        now = datetime.now()
                        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                        data1 = {'status':"Stream URL is invalid!",'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':"",'last_updated':True}

                        log.error('Exception in the current frame: {}'.format(data1))
                        frame_sum_arr_except.append(data1)
                        msg_py['payload'] = frame_sum_arr_except    # this will be displayed in fronted using socket
                        msg_passing.append(msg_py)
                        vid.release()

                        return msg_py
                    vid.release()
                except Exception as e:
                    log.error('Video Capture Exception: {}'.format(e))
                    log.error("Stream URL is invalid")

                    now = datetime.now()
                    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                    data1 = {'status':"Stream URL is invalid!",'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':"",'last_updated':True}

                    log.error('Exception in the current frame: {}'.format(data1))
                    frame_sum_arr_except.append(data1)
                    msg_py['payload'] = frame_sum_arr_except    # this will be displayed in fronted using socket
                    msg_passing.append(msg_py)
                    vid.release()

                    return msg_py

            import os
            import shutil

            if os.path.exists(cfg.output_path+video_name):
                 shutil.rmtree(cfg.output_path+video_name)  #remove directory even it contains files inside
                 log.warn('{} folder removed'.format(video_name))

            if not os.path.exists(cfg.output_path+video_name):
                 os.makedirs(cfg.output_path+video_name)
                 log.warn('{} folder created'.format(video_name))

            frame_num = 0
            cnt = 0
            keep_trying = True
            try:
                # while video is running
                while keep_trying == True:
                        detection_type_mask = "no_mask"
                        detection_type_weapon =  "no_weapon"
                        weapon_arr = [] #here after each loop weapon_arr should be made empty to reduce the memory consumption

                        if (video_ext in ['mp4','webm']):

                            log.debug("Reading video frame {}".format(frame_num))
                            return_value, frame = vid.read()

                            if return_value:
                                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                #image = Image.fromarray(frame)
                            else:

                                if frame_num !=0:   # if video format issue frame_num will be 0. if >0 then it is coming after inference is completed
                                    #after inference completed do this
                                    log.info("Ended video inference here")

                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

                                    data1 = {'status':'Completed','video_name':video_friendly_name,'video_type':video_ext,'datetime':dt_string,'Threat_status':"",'last_updated':True} #send to cocket
                                    arr_comp = []
                                    arr_comp.append(data1)
                                    #print("arr_comp",arr_comp)
                                    msg_py['payload'] = arr_comp    # this will be displayed in fronted using socket
                                    msg_passing.append(msg_py)

                                    return msg_py
                                else: #if any exception in reading video when reading the frame go inside this elif
                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                                    data1 = {'status':"Video URL is invalid!",'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':"",'last_updated':True}

                                    log.error('Exception in the current frame: {}'.format(data1))
                                    frame_sum_arr_except.append(data1)
                                    msg_py['payload'] = frame_sum_arr_except    # this will be displayed in fronted using socket
                                    msg_passing.append(msg_py)

                                    return msg_py

                        elif (video_ext in ['rtsp','mjpeg']):
                                try:
                                    #print('Reading stream')
                                    return_val,frame = vid_latest_rtsp.read()
                                    log.debug("RETURN VALUE: {}".format(return_val))
                                    #if we are not getting any frames at the middle , we re assign the video capture
                                    if not return_val:
                                        cnt += 1
                                        log.debug("No return value count: {}".format(cnt))
                                        if cnt > cfg.bad_frame_skip_size:
                                            vid_latest_rtsp = cv2.VideoCapture(video_path)
                                            cnt = 0
                                            log.info("within cnt > {}".format(cfg.bad_frame_skip_size)) 

                                        continue

                                    if frame is None:
                                        continue
                                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    #image = Image.fromarray(frame)
                                    cnt_false = 0   # if comes inside try after going to exception make count again 0.
                                except Exception as e:
                                    #rtsp stream can break due to network issue. so w8 for 1 sec and check return_value is True. Else exit.
                                    log.error("Video delay: {}".format(e))

                        frame_num +=1
                        if frame_num%cfg.frame_skip_size!=0:
                            continue

                        if (video_ext in ['mp4','webm']):
                            log.info("Frame #: {} of {}".format(frame_num, frame_count))
                        else:
                            log.info("Frame #: {}".format(frame_num))

                        #start = time.time()
                        image,start_time2,end_time2,scores_weapon,classes_weapon = inference_images_weapon(frame,video_name,frame_num)  #inference
                        #time_taken = (time.time() - start )
                        fps = 1.0 / (time.time() - start_time2)
                        log.info("FPS01: %.2f" % fps)
                        #Converting tensor to numpy array
                        scores_weapon = tf.make_ndarray(tf.make_tensor_proto(scores_weapon) )
                        classes_weapon = tf.make_ndarray(tf.make_tensor_proto(classes_weapon) )

                        image_capture_path = ""
                        weapon_threats_in_frame = []
                    
                    #weapon json to show frames where weapons detected
                        for s,c in zip(scores_weapon[0],classes_weapon[0]):

                            if (float(s)>0):
                                if (int(c)==0):
                                    detection_class  = 'Gun : '+str(s)   #Added score for prediction also
                                elif (int(c)==1):
                                    #check whether the score is greater than knife threshold. added this since model predicts other objects as knife
                                    if float(s) > knife_threshold:
                                        detection_class  = 'Knife : '+str(s)  #Added score for prediction also
                                    else:
                                        continue
                                elif (int(c)==2):
                                    detection_class  = 'Rifle : '+str(s)  #Added score for prediction also
                                else:
                                    detection_class = 'None'
                                weapon_threats_in_frame.append(detection_class)
                                threat_status = 'Threat detected | Weapon:'+ str(weapon_threats_in_frame)
                                detection_type_weapon = 'Weapon Detected |'+ detection_class
                                #print(detection_type_weapon)
                                if (video_ext in ['mp4','webm']):
                                    time_taking = frame_num/fps         #calculate the video time
                                    image1_write = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                                    image_capture_path = 'weapon_'+str(round(time_taking,2))+'.jpg'
                                    cv2.imwrite(cfg.output_path + video_name + '/' + image_capture_path, image1_write)
                                    weapon_arr.append(image_capture_path)
                                    data_weapon = {'status':detection_type_weapon,'video_name':video_name1,'time(s)':str(round(time_taking,2)),'Threat_status':threat_status,'image_path':image_capture_path,'weapon_images':weapon_arr}
                                elif (video_ext in ['rtsp','mjpeg']):
                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                                    image1_write = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                                    image_capture_path = 'weapon_'+dt_string+'.jpg'
                                    cv2.imwrite(cfg.output_path + video_name + '/' + image_capture_path, image1_write)
                                    weapon_arr.append(image_capture_path)
                                    data_weapon = {'status':detection_type_weapon,'video_name':video_name1,'datetime':dt_string,'Threat_status':threat_status,'image_path':image_capture_path,'weapon_images':weapon_arr}

                                msg_py['payload'] = data_weapon
                                msg_py['data_weapon'] = data_weapon
                                msg_passing.append(msg_py)

                                log.info("After sending the input")
                                data_weapon = json.dumps(data_weapon)
                                with open(cfg.output_path + video_name + '/' + video_name+'_weapon.json', 'w+') as f:
                                    f.write(data_weapon)
                                    f.flush()
                                    f.close()
                                push.do_push(data_weapon)
                                break
                                log.info("After writing the input")


                        img = Image.fromarray(image.astype("uint8"))
                        log.info("After fetching img")
                        rawBytes = io.BytesIO()
                        img.save(rawBytes, "JPEG")
                        rawBytes.seek(0)
                        img_base64 = base64.b64encode(rawBytes.getvalue()).decode('ascii')
                        # print('img_base64',img_base64)
                        mime = "image/jpeg"
                        uri = "data:%s;base64,%s"%(mime, img_base64)

                        now = datetime.now()
                        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

                        #if weapon or robbery mask detected then threat detected.
                        if (detection_type_mask=='no_mask') and (detection_type_weapon=='no_weapon'):
                            threat_status = 'Threat not detected'
                        else:
                            threat_status = 'Threat detected | Weapon:'+ str(weapon_threats_in_frame)

                        status = 'video processing'

                        #send this json to show threats in real time via socket
                        data1 = {'status':status,'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':threat_status,'last_updated':True}

                        #send this json with frame to show video in real time
                        data2 = {'status':status,'video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':threat_status,'frame':uri,'image_path':image_capture_path,"building":building}


                        #send last 10 threats summary ## start
                        if threat_status != 'Threat not detected':
                            frame_sum_arr.append(data1)
                            if len(frame_sum_arr) <= 10:    #only update last update key for 1st 10 frames
                                if len(frame_sum_arr)!=0:
                                    frame_sum_arr_new = []          #change old frames last_updated status false and only keep for last frame as True
                                    for dic in  frame_sum_arr[0:len(frame_sum_arr)-1]:
                                        data_old = {'status':dic['status'],'video_name':dic['video_name'],'video_type':dic['video_type'],'datetime':dic['datetime'],'Threat_status':dic['Threat_status'],'last_updated':False}
                                        frame_sum_arr_new.append(data_old)
                                frame_sum_arr = frame_sum_arr_new
                                frame_sum_arr.append(data1)    #for 5th element  append data1
                                log.warn("{} Detected in Frame: {}".format(detection_class, str(frame_num)))
                            elif len(frame_sum_arr) == 11:   # if lenth is 11 remove 1st element keep only last 10 elements. Also update last_update key
                                frame_sum_arr_new = []


                                #update last_update key
                                for dic in  frame_sum_arr[1:len(frame_sum_arr)-1]:
                                        data_old = {'status':dic['status'],'video_name':dic['video_name'],'video_type':dic['video_type'],'datetime':dic['datetime'],'Threat_status':dic['Threat_status'],'last_updated':False}
                                        frame_sum_arr_new.append(data_old)
                                frame_sum_arr = frame_sum_arr_new
                                frame_sum_arr.append(data1)

                            #print("no of frames : {} and frame_sum_arr : {}".format(len(frame_sum_arr), frame_sum_arr))
                            #send last 10 threats summary ## end

                            #save only the video clip when the threat is detected start

                            if (video_ext in ['mp4','webm']):
                                output_format = 'vp80'
                                log.info("output assignment. format{} path:{}".format(output_format, cfg.output_path))
                                output_path_set = True
                                output_path = cfg.output_path+video_name+'/'+detection_class+'_'+str(time_taking)+'.webm'
                                # by default VideoCapture returns float instead of int
                                width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                                height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                fps = int(vid.get(cv2.CAP_PROP_FPS))
                                codec = cv2.VideoWriter_fourcc(*output_format)
                                # out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
                                out = cv2.VideoWriter(output_path, codec, fps/5, (width, height))



                        msg_py['payload'] = frame_sum_arr    # this will be displayed in fronted using socket
                        msg_passing.append(msg_py)
                        msg_py['payload'] = data2 #send frame to show video in real time in frontend
                        msg_passing.append(msg_py)

                        #only save frame for mp4 or webm videos
                        if (video_ext in ['mp4','webm']):
                            fps = 1.0 / (time.time() - start_time2)
                            log.info("FPS02: %.2f" % fps)
                            result = np.asarray(image)
                            # cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
                            result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                            ##write the video inside   ./detections/detections_flask
                            if output_path_set:
                                out.write(result)

                        elif (video_ext in ['rtsp','mjpeg']):
                            if int(time.time()) > stream_read_stop_time:
                                keep_trying = False
                
                #######END INFERENCE
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                status = 'Video writing completed'
                user_json={'status':status,'video_name':video_name1,'datetime':dt_string}
                #print('user_json',user_json)
                msg_py['payload'] = user_json

                #For videos inference and save full video. for RTSP streams save last 5 mins frames
                if (video_ext in ['mp4','webm']):
                    #print("Video writing completed for video ",video_name1)

                    ##############update common json saying that video inference completed##############
                    data1 = {'status':'video completed','video_name':video_name1,'video_type':video_ext,'datetime':dt_string,'Threat_status':threat_status}

                    log.info('Python function ended. Video inference completed')

                elif (video_ext in ['mjpeg','rtsp']):
                        log.info('Python function ended. Stream inference completed')

                keep_trying = False


            except Exception as e:
                log.error("Process exception occurred in  video inferencing : {}".format(e))
                keep_trying = False
            
            InteractiveSession.close(session)
            # ssession.close()
            return msg_py

