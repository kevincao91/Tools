#-*-coding:utf-8-*-
import sys
import os
import cv2
import shutil
from tqdm import tqdm
 
THRESHOLD = 5.0
 
img_root = r'/media/kevin/DataSet/xizang_database/youtube/sample_videos_outputs'
dst_root = r'/media/kevin/DataSet/xizang_database/youtube/mohu'
for root, dirs, fs in os.walk(img_root):
    print(root, dirs)
    i = 0
    find_img_list = []
    for f in tqdm(fs):
        item = os.path.join(root, f)
        image = cv2.imread(item)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageVar = cv2.Laplacian(gray, cv2.CV_64F).var()
        #print(imageVar)
        if imageVar < THRESHOLD:
            print(imageVar)
            find_img_list.append(item)
            print(item)
            cv2.imshow('img',image)
            if cv2.waitKey(1000) & 0xFF == ord('q'): break

if len(find_img_list) >= 1:
    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)
    for item in find_img_list:
        dst_path = os.path.join(dst_folder, item.split('/')[-1])
        shutil.copy(item, dst_path)
