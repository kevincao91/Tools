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
import os,shutil,math
import numpy as np
import time
from tqdm import tqdm
from basicFun import FILES,IMG,XML
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
    baseObjs=XML.read_objects(baseXml)
    checkObjs=XML.read_objects(checkXml)
    for checkObj in checkObjs:
        if checkObj['name'] in forceFetch:
            return 0
    labelNumber+=len(baseObjs)+len(checkObjs)
    pairs,baseSoles,checkSoles=match_labels(baseObjs,checkObjs)
    # 2. Calculate similarity of each pair labels which containing roi similarity and location similarity
    availablePairLenth=len(pairs)
    # for pair in pairs:
    #     if pair[0]['name'] in ignoreLabels:
    #         availablePairLenth-=1
    if availablePairLenth>0:
        similarity=pair_similarity(pairs,baseName,checkName)
        for baseSole in baseSoles:
            scoreSoles+=1/weight[baseSole['name']]
        for checkSole in checkSoles:
            scoreSoles+=1/weight[checkSole['name']]

        print('mother={}+{}+{}'.format(availablePairLenth,scoreSoles,scoreSoles))
        similarity=similarity/(availablePairLenth+scoreSoles+scoreSoles)
        return similarity
    else:
        # print(baseSole)
        # print(checkSole)
        return 0

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
def pair_distance(baseObj,checkObj):
    box1=[int(obj1['xmin']),int(obj1['ymin']),int(obj1['xmax']),int(obj1['ymax'])]
    box2=[int(obj2['xmin']),int(obj2['ymin']),int(obj2['xmax']),int(obj2['ymax'])]
    width1 = abs(box1[2] - box1[0])
    height1 = abs(box1[1] - box1[3])  # 这里y1-y2是因为一般情况y1>y2，为了方便采用绝对值
    width2 = abs(box2[2] - box2[0])
    height2 = abs(box2[1] - box2[3])
    area1=width1*height1
    area2=width2*height2
    distance_a=max(area1,area2)/min(area1,area2)
    distance_l=max(abs(box1[0]-box2[0]),abs(box1[1]-box2[1]),abs(box1[2]-box2[2]),abs(box1[3]-box2[3]))
    standard=math.sqrt(max(width1,width2)*max(height1,height2))
    distance=distance_a*distance_l/standard
def match_labels(baseObjs,checkObjs):
    pairs=[]
    baseSole=[]
    for baseObj in baseObjs:
        maxiou=0
        for checkObj in checkObjs:
            if baseObj['name']==checkObj['name']:
                iou=get_iou(baseObj,checkObj)
                if iou>maxiou :
                    matchLabel=checkObj
                    maxiou=iou
        if maxiou>0.2:
            pairs.append((baseObj,matchLabel))
        else:
            baseSole.append(baseObj)  
    for pair in pairs:
        if pair[1] in checkObjs:
            checkObjs.remove(pair[1])
    return pairs,baseSole,checkObjs
featureArea=[]
# featureArea=(806,348,1123,525) 
if __name__=="__main__":
    # imgDir='/disk2/hao.yang/pyFiles/labels/'
    # xmlDir=imgDir
    THRESH=0.2
    record={}
    weight={'blue':0.3,'yellow':2,'other':0.5,'red':0.3,'tank_open':1,'tank_close':1,'pipe_on':1,'clamp_on':1,'jug':1,'outfire':0.5,
    'tanker':1,'hole':0.3,'tube':0.3,'gray':-10,'vehicle':1}
    forceFetch=[]
    print(weight)
    imgDir='/disk2/hao.yang/project/Qin/data/preProcess/extractFrame/0525/0525_unload_total/0525_unloadAll_total_spec/'
    xmlDir='/disk2/hao.yang/project/Qin/data/preProcess/extractFrame/0525/0525_unload_total/0525_unloadAll_total_spec/'
    if imgDir[-1]=='/':
        abandonDir=imgDir[:-1]+"_abandon"
        difDir=imgDir[:-1]+"_dif"
    else:
        abandonDir=imgDir+"_abandon"
        difDir=imgDir+"_dif"
    FILES.rm_mkdir(abandonDir)
    FILES.rm_mkdir(difDir)
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if '.xml' in x]
    begin=0
    labelNumber=0
    difNumber=0
    resume=0
    for xmlName in tqdm(allXmls):
        checkName=xmlName
        if resume<0:
            resume+=1
            continue
        if begin == 0:
            baseName = checkName
            begin = 1
            continue
        similarity=calculate_similarity_on_labels(baseName,checkName)
        cord=max(int(similarity*10),0)
        if cord not in record.keys():
            record[cord]=1
        else:
            record[cord]+=1
        # print(record)
        if similarity>THRESH:
            checkImg=os.path.join(imgDir,checkName.replace('.xml','.jpg'))
            abandonImg=os.path.join(abandonDir,checkName.replace('.xml','.jpg'))
            shutil.copy(checkImg,abandonImg)
            baseImg=os.path.join(imgDir,baseName.replace('.xml','.jpg'))
            abandonImg=os.path.join(abandonDir,baseName.replace('.xml','.jpg'))
            shutil.copy(baseImg,abandonImg)
        else:
            checkImg=os.path.join(imgDir,checkName.replace('.xml','.jpg'))
            difImg=os.path.join(difDir,checkName.replace('.xml','.jpg'))
            shutil.copy(checkImg,difImg) 
            baseName = checkName
