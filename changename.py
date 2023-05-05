# coding: utf-8
"""
    将原始数据集进行划分成训练集、验证集和测试集
"""

import os
import glob
import random
import shutil

data_dir = '/media/kevin/娱乐/weather_database/two_weather_database'
out_dir = '/media/kevin/娱乐/weather_database/testdata/1101/merage'

def makedir(new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def merage(typestr):

    for root, dirs, files in os.walk(typestr):
        for dir_ in dirs:
            imgs_list = glob.glob(os.path.join(root, dir_, '*.jpg'))
            num_max = len(imgs_list)
            for idx, img in enumerate(imgs_list):
                out_path = os.path.join(out_dir, dir_ + '_' + os.path.split(img)[-1])
                shutil.copy(os.path.join(root, dir_, img), out_path)
                
                if idx % 1000 == 0:
                    print(idx, num_max)


if __name__ == '__main__':
    makedir(out_dir)
    merage(data_dir)


