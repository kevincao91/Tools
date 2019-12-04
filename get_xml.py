#!/usr/bin/env python
# author: hao.pan
# data: 2019/08/05
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import glob
import logging
import os
import sys
import time
import numpy as np
from lxml import etree, objectify

from caffe2.python import workspace

from detectron.core.config import assert_and_infer_cfg
from detectron.core.config import cfg
from detectron.core.config import merge_cfg_from_file
from detectron.utils.io import cache_url
from detectron.utils.logging import setup_logging
from detectron.utils.timer import Timer
import detectron.core.test_engine as infer_engine
import detectron.datasets.dummy_datasets as dummy_datasets
import detectron.utils.c2 as c2_utils
import detectron.utils.vis as vis_utils

c2_utils.import_detectron_ops()
cv2.ocl.setUseOpenCL(False)

def create_new_anno(file_name, w, h):
    name=str(file_name)
    
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('a'),
        E.filename(name),
        E.source(
            E.database('oil'),
        ),
        E.size(
            E.width(int(w)),
            E.height(int(h)),
            E.depth(3)
        ),
        E.segmented(0)
    )
    return anno_tree

def create_new_obj(obj_name,x1,y1,x2,y2):
    rec_name= str(obj_name)
    E2 = objectify.ElementMaker(annotate=False)
    anno_tree2 = E2.object(
        E2.name(rec_name),
        E2.bndbox(
            E2.xmin(x1),
            E2.ymin(y1),
            E2.xmax(x2),
            E2.ymax(y2)
        ),
        E2.difficult(0)
    )
    return anno_tree2

def make_xml_file(par,res,w,h,file_name):
    cate_list=par['category_list']
    obj_nums=len(res)

    tree=create_new_anno(file_name,w,h)
    for i in range(obj_nums):
        obj_name=cate_list[int(res[i][0])]
        xmin=int(res[i][1])
        ymin=int(res[i][2])
        xmax=int(res[i][3])
        ymax=int(res[i][4])
        #print(obj_name,xmin,ymin,xmax,ymax)
        obj_tree=create_new_obj(obj_name,xmin,ymin,xmax,ymax)
        tree.append(obj_tree)

    etree.ElementTree(tree).write(file_name, pretty_print=True)


    
def infer(par,thresh):
    logger = logging.getLogger(__name__)
    merge_cfg_from_file(par['config_path'])
    cfg.NUM_GPUS = 1
    par['weight_path'] = cache_url(par['weight_path'], cfg.DOWNLOAD_CACHE)
    assert_and_infer_cfg(cache_urls=False)

    assert not cfg.MODEL.RPN_ONLY, \
        'RPN models are not supported'
    assert not cfg.TEST.PRECOMPUTED_PROPOSALS, \
        'Models that require precomputed proposals are not supported'

    model = infer_engine.initialize_model_from_cfg(par['weight_path'])

    if os.path.isdir(par['input_img_path']):
        im_list = glob.iglob(par['input_img_path'] + '/*.jpg')
    else:
        im_list = [par['input_img_path']] 

    count = 0
    t_total = 0
    np.set_printoptions(suppress=True) #numpy不以科学计数法输出
    for i, im_name in enumerate(im_list):# i为计数，im_name为图像路径
        out_name = os.path.join(
            par['output_xml_path'], '{}'.format(os.path.basename(im_name.rstrip(".jpg")) + '.xml')
        )
        #logger.info('Processing {} -> {}'.format(im_name, out_name))
        im = cv2.imread(im_name)
        w = float(im.shape[1])
        h = float(im.shape[0])
        #开始计时
        timers = defaultdict(Timer)
        t_start = time.time()
        with c2_utils.NamedCudaScope(par['gpu_id']):
            cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
                model, im, None, timers=timers
            )
        boxes, segms, keypoints, classes = vis_utils.convert_from_cls_format(cls_boxes, cls_segms, cls_keyps)
        if boxes is not None:
            boxes = np.array(boxes)
            # 坐标归一化 ↓
            # boxes[:,0:4] = boxes[:,0:4]/np.array([col,row,col,row])
            # boxes = np.maximum(boxes,0)
            # boxes = np.minimum(boxes,1)
            classes_ = np.array(classes,dtype=int)
            classes_temp = classes_.reshape(1,-1)
            classes = np.transpose(classes_temp)
            res = np.hstack((classes,boxes))  # res中，第一列为类别，2~5列为坐标，第六列为分数
            res = res[res[:,-1]>thresh]
        else:
            res = []
        #结束计时
        t_end = time.time()
        t_total = t_total + (t_end-t_start)
        count = count + 1
        make_xml_file(par,res,w,h,out_name)
    print("Average detection time:",int(1000*t_total/count),"ms/img")



if __name__ == '__main__':
    labelmap_car={1:'car',}
    labelmap_checkout={1:'blue',2:'yellow',3:'other',4:'hand',5:'phone',6:'scanner',7:'pos_free',8:'pos_use',9:'bill',10:'card'}
    labelmap_eRoom={1:'blue',2:'yellow',3:'other',4:'red',5:'ebox_close',6:'ebox_open'}
    labelmap_isle={1:'blue',2:'yellow',3:'other',4:'red',5:'car',6:'truck',7:'bus',8:'motorcycle',9:'oilgun',10:'cover'}
    labelmap_gate={1:'blue',2:'yellow',3:'other'}
    labelmap_guide={1:'blue',2:'yellow',3:'other',4:'red',5:'car',6:'truck',7:'bus',8:'motorcycle',9:'oilgun',10:'neat',11:'mess'}
    labelmap_safe={1:'blue',2:'yellow',3:'other',4:'security',5:'safe_close',6:'safe_hide',7:'safe_open',8:'door_close',9:'door_open',10:'cashbox_close',11:'cashbox_open'}
    labelmap_unload={1:'blue',2:'yellow',3:'other',4:'red',5:'tank_open',6:'tank_close',7:'pipe_on',8:'clamp_on',9:'jug',10:'outfire',11:'tanker',12:'hole',13:'tube',14:'gray',15:'vehicle'}
#----------------------------------------
    # 置信度
    thresh=0.7
    # 选择显卡
    gpu_id=0
    # 输入图片文件夹路径
    input_img_path="/DATACENTER2/ke.cao/tool/unload_images"
    # 输出xml文件夹路径
    output_xml_path="/DATACENTER2/ke.cao/tool/unload_images_xml"
    # 模型权重路径
    weight_path="/DATACENTER3/hao.pan/project_model/oil/oil_shanxi/unload/0806/8-6_unload.pkl"
    # 配置文件路径
    config_path="/DATACENTER3/hao.pan/project_model/oil/oil_shanxi/unload/0806/8-6_unload.yaml"

    par={'input_img_path':input_img_path,
         'output_xml_path':output_xml_path,
         'weight_path':weight_path,
         'config_path':config_path,
         'gpu_id':gpu_id,
         'category_list':labelmap_unload}
#----------------------------------------

    workspace.GlobalInit(['caffe2', '--caffe2_log_level=0'])
    setup_logging(__name__)
    infer(par,thresh)
