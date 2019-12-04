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
from basicFun import VIDEO
def extraFrames(oneCamera,boxsOneCamera):
    #仅支持一级根目录
    if not os.path.exists(boxsOneCamera):
                os.mkdir(boxsOneCamera)
    for root,dirs,files in os.walk(oneCamera):
        if root==oneCamera:
            try:
                videoFiles=files
            except:
                print("first layer having no file",root)
    for videoFile in videoFiles:
        if ".dav" in videoFile:
            videoPath=os.path.join(oneCamera,videoFile)
            boxspath=os.path.join(boxsOneCamera,videoFile.split('.')[0]+'.mp4')
            
            #print(videoPath,"transfering...")
            try:
                print('ffmpeg -i "' + videoPath + '"  "' + boxspath + '"\n')
                os.system('ffmpeg -i "' + videoPath + '"  "' + boxspath + '"\n')  # -r n 每秒取n帧
                print(time.time() - start)
                
            except:
                print("can't trans ",videoPath)
        else:
            print(videoFile,"not .dav")
    
if __name__=="__main__":
    start = time.time()
    print(start)
    aviPath=r"/DATACENTER2/yh/dataRoom/gasStation/safebox/test/video/20180425/output/instance201804030836281632_01934.avi"
    mp4Path=aviPath.split('.')[0]+'.mp4'
    VIDEO.avi2mp4(aviPath,mp4Path)
    # extraFrames(davDir,mp4Dir)
