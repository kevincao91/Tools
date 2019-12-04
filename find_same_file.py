# coding:utf-8
import os
import glob
import random
import shutil
'''
    为数据集生成对应的txt文件
'''

ori_dir = '/media/kevin/办公/xizang/testdataset/1031/JPEGImages'
tra_dir = '/media/kevin/办公/xizang/data/baidu/'
mv_dir = './mv/'


# 
def find_same_file(ori_dir, tra_dir):

    for root, dirs, files in os.walk(ori_dir):
        print(root)

        imgs_list = glob.glob(os.path.join(root, '*.jpg'))
        imgs_num = len(imgs_list)

        for i in range(imgs_num):
            file_name = imgs_list[i].split('/')[-1]
            tar_file_name = os.path.join(tra_dir, file_name)
            print(tar_file_name)
            if os.path.exists(tar_file_name):
                print('find file %s' % file_name, tar_file_name)
                srcfile = tar_file_name
                dstfile = os.path.join(mv_dir, file_name)
                shutil.move(srcfile,dstfile)          #移动文件
                print('move file %s  to %s' % (srcfile , dstfile))
            else:
                print('no file %s' % file_name)
            


  
  
if __name__ == '__main__':

    find_same_file(ori_dir, tra_dir)
    print('finish')


