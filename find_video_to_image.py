# coding=utf-8


import os
import cv2
from tqdm import tqdm
def extra_frames(videoPath,outPath,imgInfo,interval):
    catcher= cv2.VideoCapture(videoPath) #读入视频文件
    count=0
    flag=catcher.isOpened()
    img_id=0
    while flag:   #循环读取视频帧
        count = count + 1
        flag, frame = catcher.read()
        if flag and (count%interval== 0):
            img_id = img_id + 1
            file_path = outPath+imgInfo+str('%06d'%img_id) + '.jpg'
            cv2.imwrite(file_path, frame) #存储为图像
            if img_id%100 == 0:
                print('output->'+file_path)
            cv2.waitKey(1)
    catcher.release()

def getFiles(dir, suffix): # 查找根目录，文件后缀 
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename) # =>文件名,文件后缀
            if suf == suffix:
                res.append(os.path.join(root, filename)) # =>吧一串字符串组合成路径
    print(len(res), ' files')
    return res


if __name__=="__main__":


    file_list = getFiles("/media/kevin/办公/yichang/国外监控/", '.mp4')  # =>查找以.mp4结尾的文件
    outPath="/media/kevin/办公/yichang/国外监控_sample_images/"
    if not os.path.exists(outPath):
        os.mkdir(outPath)
    
    for file in file_list:
        print(file)
    print('\n')

    for i in range(len(file_list)):
        var=str(i+1)
        print(var+'/'+str(len(file_list)))
    #--------------------------------------config
        videoPath=file_list[i]
        print(videoPath)
        imgInfo='xizang_foreign_road'+'_191121_'+var
        # print(str(imgInfo))
        interval=90      # 30/1s   90/3s
	#--------------------------------------
        extra_frames(videoPath,outPath,imgInfo,interval)
