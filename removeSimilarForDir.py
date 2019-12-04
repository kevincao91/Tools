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
import os
import numpy as np
import time
import shutil
from basicFun import FILES,IMG,COCO
featureArea=[]
featureArea=COCO.ebox_coordinate
# 适用于卸油口全局去重的阈值
SIMIBOUND=0.8
# 适用于保险柜小区域去重的阈值
# SIMIBOUND=0.8
startdir=1#从第startdir开始，处理完第enddir结束（包含enddir）
enddir=43#注意作为开始的startdir第一帧无事件
# 需定义的参数：
if __name__=="__main__":
    # IMG.info()
    start = time.time()
    count = 1
    resume=1
    imgDir='/DATACENTER4/hao.yang/project/Qin/data/preProcess/removedSimilarityFrame/0603/0603_eRoom/n_modelImg/'
    # imgDir="/DATACENTER5/hao.yang/dataRoom/Qin/park/caotan/longVideoFrames/8/"
    if os.path.exists(imgDir):
        if imgDir[-1]=='/':
            difDir=imgDir[:-1]+"_dif{}".format(SIMIBOUND*100)
        else:
            difDir=imgDir+"_dif{}".format(SIMIBOUND*100)
        begin=0
        restart=1
        FILES.rm_mkdir(difDir)
        allFILES=FILES.get_sorted_files(imgDir)
        jpgsCount=len(allFILES)
        for file in allFILES:
            if ".jpg" in file:
                checkPath = os.path.join(imgDir, file)
                if restart==0:
                    continue
                if begin == 0:
                    difpath = os.path.join(difDir, file)
                    shutil.copy(checkPath, difpath)
                    basePath = checkPath
                    begin = 1
                    continue
                if count<resume:
                    count+=1
                    continue
                similar = IMG.compare_cos_featrue(basePath, checkPath, featureArea)
                print(basePath,file,similar)
                if similar<SIMIBOUND:
                    difpath=os.path.join(difDir,file)
                    shutil.copy(checkPath,difpath)
                    basePath=difpath
                print("{rate:.2f}%  tarDir={dir:}  ".format(dir=difDir,rate=100*float(count)/jpgsCount))
            count+=1
    print(time.time() - start)