#encoding=utf-8
# 代码功能：
# 去掉文件夹内相似的图片
# 需定义的参数：
# 同一个摄像头分帧的二级根目录oneCameraFrame
# 提取出的box图像保存的二级根目录boxsOneCamera
# 检测特征的checkBox
# 截取区域的extraBox
#矩阵直接相减1.6秒一张
#cos距离3秒一张
##库
import os,shutil,math,glob
import numpy as np
import time
from tqdm import tqdm
from basicFun import FILES,IMG,XML,COCO
def get_iou(obj1, obj2):
    """
    :param box1:[x1,y1,x2,y2] 左上角的坐标与右下角的坐标
    :param box2:[x1,y1,x2,y2]
    :return: iou_ratio--交并比
    """
    box1=[int(obj1['xmin']),int(obj1['ymin']),int(obj1['xmax']),int(obj1['ymax'])]
    box2=[int(obj2['xmin']),int(obj2['ymin']),int(obj2['xmax']),int(obj2['ymax'])]
    width1 = abs(box1[2] - box1[0])
    height1 = abs(box1[1] - box1[3])  # 这里y1-y2是因为一般情况y1>y2，为了方便采用绝对值
    width2 = abs(box2[2] - box2[0])
    height2 = abs(box2[1] - box2[3])
    x_max = max(box1[0], box1[2], box2[0], box2[2])
    y_max = max(box1[1], box1[3], box2[1], box2[3])
    x_min = min(box1[0], box1[2], box2[0], box2[2])
    y_min = min(box1[1], box1[3], box2[1], box2[3])
    iou_width = x_min + width1 + width2 - x_max
    iou_height = y_min + height1 + height2 - y_max
    if iou_width <= 0 or iou_height <= 0:
        iou_ratio = 0
    else:
        iou_area = iou_width * iou_height  # 交集的面积
        box1_area = width1 * height1
        box2_area = width2 * height2
        iou_ratio = iou_area / (box1_area + box2_area - iou_area)  # 并集的面积
    return iou_ratio
def calculate_similarity_on_labels(baseName,checkName):
    # 1. Match labels
    global labelNumber
    scoreSoles=0
    baseXml=os.path.join(xmlDir,baseName)
    checkXml=os.path.join(xmlDir,checkName)
    baseObjs=XML.read_objects_exclude_minsize(baseXml)
    checkObjs=XML.read_objects_exclude_minsize(checkXml)
    for checkObj in checkObjs:
        if checkObj['name'] in forceFetch:
            return 100
    labelNumber+=len(baseObjs)+len(checkObjs)
    similarity=match_labels(baseObjs,checkObjs)
    return similarity


    # 3. Set a set of special value for unmatch labels
    # 4. Return the whole similarity of two imgs 
    # if len(pairs)*2>len(baseSole)+len(checkSole):
    #     return 1
    # else:
    #     return 0
def pair_similarity(pairs,baseName,checkName):
    baseImg=os.path.join(imgDir,baseName.replace('.xml','.jpg'))
    checkImg=os.path.join(imgDir,checkName.replace('.xml','.jpg'))
    sim=0
    if os.path.exists(baseImg) and os.path.exists(checkImg):
        for pair in pairs:
            # if pair[0]['name'] not in ignoreLabels:
            baseRoi=(int(pair[0]['xmin']),int(pair[0]['ymin']),int(pair[0]['xmax']),int(pair[0]['ymax']))
            checkRoi=(int(pair[1]['xmin']),int(pair[1]['ymin']),int(pair[1]['xmax']),int(pair[1]['ymax']))
            sim+=IMG.img_cos_for_labels(baseImg,checkImg,baseRoi,checkRoi)*weight[pair[0]['name']]
    return sim
def pair_distance(obj1,obj2):
    box1=[int(obj1['xmin']),int(obj1['ymin']),int(obj1['xmax']),int(obj1['ymax'])]
    box2=[int(obj2['xmin']),int(obj2['ymin']),int(obj2['xmax']),int(obj2['ymax'])]
    width1 = abs(box1[2] - box1[0])
    height1 = abs(box1[1] - box1[3])  # 这里y1-y2是因为一般情况y1>y2，为了方便采用绝对值
    width2 = abs(box2[2] - box2[0])
    height2 = abs(box2[1] - box2[3])
    area1=width1*height1
    area2=width2*height2
    distance_a=min(max(area1,area2)/min(area1,area2),2)
    distance_l=max(abs(box1[0]-box2[0]),abs(box1[1]-box2[1]),abs(box1[2]-box2[2]),abs(box1[3]-box2[3]))
    standard=math.sqrt(max(width1,width2)*max(height1,height2))
    distance=distance_a*distance_l/standard*weight[obj1['name']]
    if obj1['name'] in COCO.areaNames:
        distance=distance*min(area1/2000.0,2.0)
    return distance
def match_labels(baseObjs,checkObjs):
    global t
    pairs=[]
    baseSole=[]
    maxMatchDis=0
    if t>0:
        print(1)
    for baseObj in baseObjs:
        minPairDis=100
        match=0
        for checkObj in checkObjs:
            if baseObj['name']==checkObj['name']:
                match=1
                pariDistance=pair_distance(baseObj,checkObj)
                if pariDistance<minPairDis:
                    minPairDis=pariDistance
        # minPairDis: baseObj与checkObjs所有配对组的最小间距
        if match>0 and minPairDis>maxMatchDis:
            maxMatchDis=minPairDis
        # maxMatchDis: 所有baseObjs最小配对间距之中的最大值
        elif match==0:
            maxMatchDis+=weight[baseObj['name']]
    for checkObj in checkObjs:
        minPairDis=100
        match=0
        for baseObj in baseObjs:
            if baseObj['name']==checkObj['name']:
                match=1
                pariDistance=pair_distance(baseObj,checkObj)
                if t>0:
                    print(pariDistance)
                    t=0
                if pariDistance<minPairDis:
                    minPairDis=pariDistance
        if match>0 and minPairDis>maxMatchDis:
            maxMatchDis=minPairDis
        elif match==0:
            maxMatchDis+=weight[checkObj['name']]          
    return maxMatchDis
featureArea=[]
# featureArea=(806,348,1123,525) 
if __name__=="__main__":
    task='unload'
    THRESH=0.8
    # THRESH=getattr(COCO,'thresh_{}'.format(task))
    # THRESH=1
    record={}
    weight=getattr(COCO,'weight_{}'.format(task))
    forceFetch=[]
    # forceFetch=['scanner','cover']
    print(THRESH)
    print(weight)
    imgDir='/DATACENTER2/ke.cao/oil_video_Data/unload_images_dif_day/day_1/'
    xmlDir='/DATACENTER2/ke.cao/oil_video_Data/unload_images_dif_day/day_1_xml_fixed/'
    if imgDir[-1]=='/':
        errorDir=imgDir[:-1]+"_error"
        difDir=imgDir[:-1]+"_dif"
    else:
        errorDir=imgDir+"_error"
        difDir=imgDir+"_dif"
    if xmlDir[-1]=='/':
        difXmlDir=xmlDir[:-1]+"_dif"
    else:
        difXmlDir=xmlDir+"_dif"
    print(xmlDir)
    FILES.rm_mkdir(difXmlDir)   
    FILES.rm_mkdir(difDir)
    # allXmls=[x for x in FILES.get_sorted_files(xmlDir) if '.xml' in x]
    allXmls=[x.replace('.jpg','.xml') for x in FILES.get_sorted_files(imgDir) if '.jpg' in x]
    begin=0
    labelNumber=0
    difNumber=0
    resume=0
    t=0
    baseTitle='baseTitle'
    print(len(allXmls))
    for xmlName in tqdm(allXmls):
        curTitle=xmlName.split('_000')[0]
        if '.' not in curTitle:
            checkTitle=curTitle
        else:
            checkTitle=baseTitle
        checkName=xmlName
        if resume>0:
            resume-=1
            continue
        if begin == 0:
            baseName = checkName
            begin = 1
            continue
        if checkTitle !=baseTitle:
            distance=1000
            baseTitle=checkTitle
        else:
            distance=100
            try:
                distance=calculate_similarity_on_labels(baseName,checkName)
            except:
                FILES.mkdir(errorDir)
                checkImg=os.path.join(imgDir,checkName.replace('.xml','.jpg'))
                errorImg=os.path.join(errorDir,checkName.replace('.xml','.jpg'))
                checkXml=os.path.join(xmlDir,checkName)
                errorXml=os.path.join(errorDir,checkName)
                shutil.copy(checkImg,errorImg) 
                shutil.copy(checkXml,errorXml) 
                baseImg=os.path.join(imgDir,baseName.replace('.xml','.jpg'))
                errorImg=os.path.join(errorDir,baseName.replace('.xml','.jpg'))
                baseXml=os.path.join(xmlDir,baseName)
                errorXml=os.path.join(errorDir,baseName)
                shutil.copy(baseImg,errorImg) 
                shutil.copy(baseXml,errorXml) 
            cord=max(int(distance*10),0)
            if cord not in record.keys():
                record[cord]=1
            else:
                record[cord]+=1
        # print(record)
        if distance<THRESH:
            checkImg=os.path.join(imgDir,checkName.replace('.xml','.jpg'))
        else:
            checkImg=os.path.join(imgDir,checkName.replace('.xml','.jpg'))
            difImg=os.path.join(difDir,checkName.replace('.xml','.jpg'))
            if os.path.exists(checkImg):
            	shutil.copy(checkImg,difImg) 
            checkxml=os.path.join(xmlDir,checkName)
            difxml=os.path.join(difXmlDir,checkName)
            shutil.copy(checkxml,difxml) 
            baseName = checkName
    # 获取提取后文件数
    path_file_list=glob.glob(os.path.join(difXmlDir,'*.xml'))  #指定文件下个数
    print(len(path_file_list))

