#! /usr/bin/env python

import multiprocessing

#print("multiprocessing part got imported in main script")

#from WeaponDetectionImports.core.functions import *

from easydict import EasyDict as edict

#from wep.core.config import cfg
#from testdir.t1 import tester

#tester()

# __C                           = edict()
# cfg                           = __C
# __C.YOLO                      = edict()
# __C.YOLO.CLASSES              = "./data/classes/weapons.names"

# # utils.read_class_names(cfg.YOLO.CLASSES)

# print(__C)

# if __name__ == '__main__':
# 	run()

import cv2
#print(cv2.__version__)

import sys
#print (sys.argv, len(sys.argv))

if len(sys.argv) == 1:
	print('Enter path to video file')
else:
	cap = cv2.VideoCapture(sys.argv[1])
	length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	print("Number of frames in '{}': {}".format(sys.argv[1], length))

