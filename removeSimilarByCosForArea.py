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
from basicFun import FILES
from basicFun import IMG
featureArea=[]
#lhTankSimi
# featureArea=(201,357,614,831)
#jnbTankSimi
# featureArea=(673,10,1205,1015)
# safe_caotan
# featureArea=(441,144,560,269)
# trade_zhangbabeilu_half
# featureArea=(638,418,674,461)
# trade_zhangbabeilu_total
# featureArea=(639,421,681,490)   
# safe_XiWan
# featureArea=(843,253,1049,481)   
# 适用于卸油口全局去重的阈值
SIMIBOUND=0.99
# 适用于保险柜小区域去重的阈值
# SIMIBOUND=0.8
jpgRoot=r"/disk2/hao.yang/project/Qin/data/preProcess/extractFrame/0522_XiWan_b/"
# if jpgRoot[-1]=='/':
#     dstRoot=jpgRoot[:-1]+"Unique"+str(int(SIMIBOUND*1000))
# else:
#     dstRoot=jpgRoot+"Unique"+str(int(SIMIBOUND*1000))
# dstRoot=jpgRoot.replace('0505','0505removedSimilarityFrame')
dstRoot=jpgRoot.replace('extractFrame','removedSimilarityFrame')
rootsName=FILES.get_sub_dirs(jpgRoot)
# rootsName=[1]
startdir=1#从第startdir开始，处理完第enddir结束（包含enddir）
enddir=43#注意作为开始的startdir第一帧无事件
# 需定义的参数：
if __name__=="__main__":
    # IMG.info()
    start = time.time()
    count = 1
    resume=1
    dirCount=1
    FILES.mkdir(dstRoot)
    for rootName in rootsName:
        dirpath=os.path.join(jpgRoot,rootName)
        # dirpath="/DATACENTER5/hao.yang/dataRoom/Qin/park/caotan/longVideoFrames/8/"
        if os.path.exists(dirpath):
            difdirpath=dirpath.replace('extractFrame','removedSimilarityFrame')
            # if difdirpath[-1]=='/':
            #     difdirpath=difdirpath[:-1]+"Unique"+str(int(SIMIBOUND*1000))
            # else:
            #     difdirpath=difdirpath+"Unique"+str(int(SIMIBOUND*1000))
            if dirCount<startdir:
                dirCount += 1
                continue
            if dirCount>enddir:
                break
            begin=0
            restart=1
            FILES.rm_mkdir(difdirpath)
            allFILES=FILES.get_sorted_files(dirpath)
            jpgsCount=len(allFILES)
            for file in allFILES:
                if ".jpg" in file:
                    # basePath='/DATACENTER5/hao.yang/dataRoom/Qin/trade/zhangbabeilu/29AD13E0_1552790204_1_000061.jpg'
                    checkPath = os.path.join(dirpath, file)
                    # print(checkPath)
                    if 'shgjihsjkghj' in file:
                        restart=1
                    if restart==0:
                        continue
                    if begin == 0:
                        difpath = os.path.join(difdirpath, file)
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
                        difpath=os.path.join(difdirpath,file)
                        shutil.copy(checkPath,difpath)
                        basePath=difpath
                    print("{rate:.2f}%  tarDir={dir:}  ".format(dir=difdirpath,rate=100*float(count)/jpgsCount))
                count+=1
        dirCount += 1
    print(time.time() - start)