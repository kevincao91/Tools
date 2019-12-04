# coding: utf-8
"""
    将原始数据集进行划分成训练集、验证集和测试集或整体成为测试集
"""
import numpy as np
import os
import glob
import random
import shutil

if not os.path.exists('./train_/'):
    os.makedirs('./train_/')
if not os.path.exists('./val_/'):
    os.makedirs('./val_/')


target_xml_root_dir = './Annotations/'

train_percent = 0.6
valid_percent = 0.4

def getFiles(dir, suffix): # 查找根目录，文件后缀 
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename) # =>文件名,文件后缀
            if suf == suffix:
                res.append(os.path.join(root, filename)) # =>吧一串字符串组合成路径
    print(len(res), ' files')
    return res


if __name__ == '__main__':

    file_list = getFiles('./Annotations/', '.xml') 

    all_num = len(file_list)
    print(all_num, 'files')

    random.seed(666)
    random.shuffle(file_list)

    train_point=round(train_percent*all_num)
    
    for idx in range(all_num):
        srcfile = file_list[idx]
        fpath,fname=os.path.split(srcfile)    #分离文件名和路径
        
        if idx<train_point:
            dstfile = os.path.join('train_',fname)
        else:
            dstfile = os.path.join('val_',fname)
        
        shutil.copy(srcfile,dstfile)          #复制文件
        # shutil.move(srcfile,dstfile)          #移动文件
        print ("copy %s -> %s"%( srcfile,dstfile))
        

    
    
    
    
