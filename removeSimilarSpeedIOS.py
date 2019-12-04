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
import os,sys
from PIL import Image
import cv2
import numpy as np
import time
import shutil
from basicFun import FILES
##库
# 需定义的参数：
SIMIBOUND=0.98
# startdir=1#从第startdir开始，处理完第enddir结束（包含enddir）
# enddir=2#注意作为开始的startdir第一帧无事件
# 需定义的参数：
def getAlldirs(path):
    for root,dirs,files in os.walk(path):
        if root==path:
            return dirs
    return []
def getAllfiles(path):
    #获取目录第一层所有文件
    for root,dirs,files in os.walk(path):
        if root==path:
            return files
    return []
def compare(basePath,framePath):
    print(basePath,framePath)
    baseImg = cv2.imread(basePath, 0)
    checkImg = cv2.imread(framePath, 0)
    baseImg = cv2.resize(baseImg,(256, 256))
    checkImg = cv2.resize(checkImg,(256, 256))
    height, width = baseImg.shape
    baseNum=0
    baseSum=0
    checkSum=0
    checkMat=[]
    baseMat=[]
    for line in range(height):
        for pixel in range(width):
            baseNum+=1
            baseSum+=baseImg[line][pixel]
    baseAve = baseSum / baseNum
    for line in range(height):
        for pixel in range(width):
            baseMat.append(baseImg[line][pixel]-baseAve)
        #print(baseAve)
    for line in range(height):
        for pixel in range(width):
            checkSum += checkImg[line][pixel]
    checkAve = checkSum / baseNum
    #print(checkAve)
    for line in range(height):
        for pixel in range(width):
            checkMat.append(checkImg[line][pixel] - checkAve)
    #print(checkMat[100])
    return cos(baseMat,checkMat)
    #计算数列的距离
def minus(baseMat,checkMat):
    baseAr=np.array(baseMat)
    checkAr=np.array(checkMat)
    

def cos(baseMat,checkMat):
    baseAr=np.array(baseMat)
    checkAr=np.array(checkMat)
    num=np.dot(baseAr,checkAr)#点积
    denom=np.linalg.norm(baseAr)*np.linalg.norm(checkAr)#模相乘
    cosValue=num/denom
    return cosValue
if __name__=="__main__":
    start = time.time()
    count = 1
    resume=1
    dirpath='/DATACENTER5/hao.yang/dataRoom/Qin/safe/caotan/data_auto/stillImg'
    if os.path.exists(dirpath):
        difdirpath=dirpath+'_rmsimilar'+str(int(SIMIBOUND*100)) #不用创建
        # for dir in alldirs:
            # if dircount<startdir:
            #     dircount += 1
            #     continue
            # if dircount>enddir:
            #     break
        begin=0
        FILES.mkdir(difdirpath)
        print(dirpath, "copyRemoving...")
        # allfiles=getAllfiles(dirpath)
        allfiles=sorted(os.listdir(dirpath))
        for file in allfiles:
            if ".jpg" in file:
                filepath = os.path.join(dirpath, file)
                print(filepath)
                if begin == 0:
                    difpath = os.path.join(difdirpath, file)
                    shutil.copyfile(filepath, difpath)
                    basepath = filepath
                    begin = 1
                    continue
                if count<resume:
                    count+=1
                    continue
                similar = compare(basepath, filepath)
                print('similar={}'.format(similar))
                print('Cost time: {:.1f} s'.format(time.time() - start))
                # 比较checkBox的相似度
                # if similar >0.9:  # 相似度太大
                #     #print(similar,basepath,filepath)
                #     os.remove(filepath)
                # else:
                #     basepath=filepath
                if similar<SIMIBOUND:
                    difpath=os.path.join(difdirpath,file)
                    shutil.copyfile(filepath,difpath)
                    basepath=filepath
                print(count)
            count+=1
    # dircount += 1
    print('Cost time: {:.1f} s'.format(time.time() - start))