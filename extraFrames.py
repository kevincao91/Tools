#encoding=utf-8
# 代码功能：
# 将视频提取为一秒一帧的jpg
# 需定义的参数：
# 视频存放二级根目录rootVideoDir
# 提取出图片保存根目录picDir
##库
import os
import time
from basicFun import FILES
def extraFrames(oneCamera,boxsOneCamera):
    #仅支持一级根目录
    for root,dirs,files in os.walk(oneCamera):
        if root==oneCamera:
            try:
                videoFiles=files
            except:
                print("first layer having no file",root)
    for videoFile in videoFiles:
        if videoType in videoFile:
            videoPath=os.path.join(oneCamera,videoFile)
            boxspath=os.path.join(boxsOneCamera,videoFile.split(videoType)[0])
            if not os.path.exists(boxspath):
                os.mkdir(boxspath)
            print(videoPath,"extracting frames...")
            try:
                os.system('ffmpeg -i "' + videoPath + '" -r 0.5 -q:v 2 -f image2 "' + boxspath + '/%06d.jpg"\n')  # -r n 每秒取n帧
            except:
                print("can't extract ",videoPath)
        else:
            print(videoFile,"not ",videoType)
if __name__=="__main__":
    start = time.time()
    print(start)
    videoType=".mp4"
    rootVideoDir=r"/DATACENTER4/hao.yang/project/Qin/data/preProcess/longVideo/"
    dirs=["0706_checkout"]
    for vDir in dirs:
        videoDir=os.path.join(rootVideoDir,vDir)
        picDir=videoDir.replace('longVideo','extractFrame')
        FILES.rm_mkdir(picDir)
        extraFrames(videoDir,picDir)
    end = time.time()
    print(end - start)
