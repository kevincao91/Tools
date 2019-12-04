import cv2
import os
import numpy as np
from PIL import Image
import shutil
import sys
import glob

changetypesflag = True
changesizeflag = False
image_size=224
#改变之后的图片尺寸

source_path=os.getcwd()+"/bing/"#等待转换的图片存放地址
types='jpg' #转换后的图片格式
target_path=os.getcwd()+"/change/"#转换过格式的图片存放地址
final_path=os.getcwd()+"/final/"#转换过格式和尺寸的图片存放地址

#如果没有转换后的图片存放文件夹，就创建对应的文件夹
if not os.path.exists(target_path):
    os.makedirs(target_path)
if not os.path.exists(final_path):
    os.makedirs(final_path)

#转变图片格式的函数
def changetypes(source_path,types):

    for root, dirs, files in os.walk(source_path):
        print(root)
        for dir_ in dirs:
            imgs_list = glob.glob(os.path.join(root, dir_, '*.*'))
            imgs_num = len(imgs_list)

            for index,pic in enumerate(imgs_list):
                try:
                    sys.stdout.write('\r>>Converting image %d/%d ' % (index, imgs_num))
                    sys.stdout.flush()
                    im = Image.open(pic)
                    traget = os.path.splitext(pic)[0] + "." + types
                    im.save(traget)
                    shutil.move(traget,target_path)
                except IOError as e:
                    print('could not read:',pic)
                    print('error:',e)
                    print('skip it\n')
            sys.stdout.write('Convert Over!\n')
            sys.stdout.flush()

#转化图片尺寸的函数
def changesize(source_path):
    image_lists=os.listdir(source_path)
    i=0
    for file in image_lists:
        i=i+1
        print(os.getcwd()+"/"+file)
        split=os.path.splitext(file)
        filename,type=split
        image_file = source_path+file
        image_source=cv2.imdecode(np.fromfile(image_file,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image_source, (image_size, image_size))
        cv2.imencode('.png',image)[1].tofile(final_path+file)

if changetypesflag:
    changetypes(source_path,types)
if changesizeflag:
    changesize(target_path)
