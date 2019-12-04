#coding: utf-8
from basicFun import modelTool
import cv2
# import cv2.cv
import detectron.utils.vis as vis_utils
import os
import sys
import shutil
from PIL import Image,ImageDraw,ImageFont
import numpy
from basicFun import XML
from basicFun import FILES
import time
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
if __name__=="__main__":
    labelmap={1:'yellow',2:'blue',3:'other',4:'security'}#gate
    inImg = "/DATACENTER2/hao.yang/project/Qin/gate/analysis/inVideoFrames/ch02_20190405172657/"
    outImg = "./outImg_one_scale"
    # FILES.rm_mkdir(outImg)
    font = cv2.FONT_HERSHEY_SIMPLEX
    CFG_PATH = "/DATACENTER2/hao.yang/project/Qin/gate/trade_faster_p150_3.yaml"
    WTS_PATH = "/DATACENTER2/hao.yang/project/Qin/gate/model/train/safe_caotan_14381_coco_train:safe_Cheng_13968_coco_train/generalized_rcnn/model_final.pkl"
    # WTS_PATH='/DATACENTER2/yh/Detectron/mission/gasStation/safe/goodModel/safe_faster_p50.pkl'
    # CFG_PATH='/DATACENTER2/yh/Detectron/mission/gasStation/safe/goodModel/safe_faster_p{}.yaml'.format(yamlName)
    testModel = modelTool.modelTool()
    testModel.initModel(CFG_PATH,WTS_PATH,labelmap)
    palette= {'yellow':(247,79,223),'blue':(0,255,255),'other':(255,247,0),
    'hand':(255,255,255),'phone':(150,84,48),'scanner':(102,0,204),
    'pos_idle':(0,0,255),'pos_use':(44,125,222),'security':(0,255,0),
    10:(1,208,169),11:(130,232,255),12:(204,153,255),
    13:(0,0,192),14:(134,225,1),0:(142,208,169)} 
    fileList = os.listdir(inImg)
    # check_speed
    statime=time.time()
    checkFrames=100
    frameIndex=0
    detect_cost=0.0
    for file in [x for x in fileList if '.jpg' in x]: 
        image = cv2.imread(os.path.join(inImg,file))
        height=image.shape[0]
        width=image.shape[1]
        top_labels,top_xmin,top_ymin,top_xmax,top_ymax,top_scores = testModel.getInfoByModel(image,0.7)
        frameIndex+=1
        sys.stdout.write('\r>> Detecting {:.1f}%'.format(100*float(frameIndex)/checkFrames))
        sys.stdout.flush()
        if frameIndex>checkFrames:
            break
    print('Cost {} s'.format(time.time()-statime))
    