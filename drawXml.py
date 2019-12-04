#encoding=utf-8
# 代码功能：
# 将dav转为mp4
# 需定义的参数：
# dav存放一级根目录davDir
# MP4保存根目录mp4Dir(不用预创建)
#1.5秒转换1M，即1500秒（约25分钟）1G，一个小时4G，10个小时40G
##库
import os
import time
from basicFun import XML
from basicFun import FILES
import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy
from basicFun import COCO

colors_tableau = [(255, 255, 255), (31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                  (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                  (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                  (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                  (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
paletteSet=[(247,79,223),(0,255,255),(255,247,0),(0,0,255),(255,255,255),(150,84,48),(102,0,204),
(44,125,222),(0,255,0),(1,208,169),(130,232,255),(204,153,255),(0,0,192),(134,225,1),(142,208,169)]
palette={}
labelmap=COCO.labelmap_isle
for i in labelmap.keys():
    palette[labelmap[i]]=paletteSet[i]
labelList={"person":0,"blue":1,"yellow":2,"other":3,"car":4,
"truck":5,"bus":6,"motorcycle":7,'oilgun':8,'cover':9}
def drawXml(image,objs):
    font_color = (255,222,0)
    for i in range(len(objs)):
        print(objs[i])
        xmin = int(objs[i]['xmin'])
        ymin = int(objs[i]['ymin'])
        xmax = int(objs[i]['xmax'])
        ymax = int(objs[i]['ymax'])
        label_name = objs[i]['name']
        color = palette[objs[i]['name']]
        cv2.rectangle(image, (xmin,ymin), (xmax, ymax), color, thickness=3)
        # font_label = ImageFont.truetype('/DATACENTER2/yh/resources/heiti.TTF',50)
        # img_PIL = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB)) # cv2==>PIL
        # draw = ImageDraw.Draw(img_PIL)
        # draw.text((xmin,ymax-50),label_name,font_color,font=font_label)
        # image = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR) # PIL==>cv2 
    # img_PIL = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB)) # cv2==>PIL
    # draw = ImageDraw.Draw(img_PIL)
    # image = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR) # PIL==>cv2    
    return image 
if __name__=="__main__":
    start = time.time()
    jpgDir=r"/disk2/hao.yang/project/Qin/data/xmls/isle/complete/imgs_overlook_16000_test/"
    xmlDir=r"/disk2/hao.yang/project/Qin/data/xmls/isle/complete/isle_FMXX_test_16000/"
    outDir=r"/disk2/hao.yang/project/Qin/data/xmls/isle/complete/imgs_overlook_16000_test_truth/"
    FILES.rm_mkdir(outDir)
    allJpgs=FILES.get_files(jpgDir)
    for jpg in allJpgs:
        # print(jpg)
        if '.jpg' in jpg:
            jpgPath=os.path.join(jpgDir,jpg)
            xmlPath=os.path.join(xmlDir,jpg.split('.')[0]+'.xml')
            objs=XML.read_objects(xmlPath)
            image = cv2.imread(jpgPath)
            img=drawXml(image,objs)
            desImg = os.path.join(outDir,jpg)
            cv2.imwrite(desImg,img)



    # extraFrames(davDir,mp4Dir)
