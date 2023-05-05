import os
from tqdm import tqdm
import shutil
import imghdr
import glob
import hashlib
import imghdr
import cv2
import numpy as np


def get_filelist(root_path): 
    original_images =[]
    for root, dirs, filenames in os.walk(root_path):
        for dir_ in dirs:
            # print('dir', dir_)
            for file in glob.glob(os.path.join(root, dir_, '*.*')):
                original_images.append(file)

    original_images = sorted(original_images)
    print('tatol num:',len(original_images))
    
    return original_images


def remove_same_piture_by_get_md5(root_path):

    original_images = get_filelist(root_path)
    
    same_img=0
    md5_list =[]
    for filename in tqdm(original_images):
        m = hashlib.md5()
        mfile = open(filename, "rb")
        m.update(mfile.read())
        mfile.close()
        md5_value = m.hexdigest()
        #print(md5_value)
        if (md5_value in md5_list):
            os.remove(filename)
            same_img+=1
        else:
            md5_list.append(md5_value)
    print('remove same images by md5:', same_img)
          
def remove_simillar_picture_by_perception_hash(path):

    original_images = get_filelist(root_path)

    hash_dic = {}
    hash_list = []
    simillar_imgs = 0
    for img_name in tqdm(original_images):
        try:
            img = cv2.imread(os.path.join(path, img_name))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            continue

        img = cv2.resize(img,(8,8))

        avg_np = np.mean(img)
        img = np.where(img>avg_np,1,0)
        hash_dic[img_name] = img
        if len(hash_list)<1:
            hash_list.append(img)
        else:
            for i in hash_list:
                flag = True
                dis = np.bitwise_xor(i,img)

                if np.sum(dis) < 5:
                    flag = False
                    os.remove(os.path.join(path, img_name))
                    simillar_imgs+=1
                    break
            if flag:
                hash_list.append(img)
    print('remove simillar imgs num:', simillar_imgs)


def is_valid_jpg(jpg_file):
    """
    判断JPG文件下载是否完整
    """
    if jpg_file.split('.')[-1].lower() == 'jpeg':
        with open(jpg_file, 'rb') as f:              
            f.seek(-2, 2)
            read_byte = f.read()
            # print(read_byte)
            if read_byte == b'\xff\xd9':
                return True
            else:
                False
    else:
        return True

def chk_valid_jpg(root_path):
    original_images = get_filelist(root_path)
    
    not_valid_jpg=0
    for filename in tqdm(original_images):
        if not is_valid_jpg(filename):
            # print(filename)
            os.remove(filename)
            not_valid_jpg+=1
    print('remove not valid jpg num:', not_valid_jpg)

def chk_error_type(root_path):

    original_images = get_filelist(root_path)
    
    error_images=0
    for filename in tqdm(original_images):
        #print(filename)
        file_end = os.path.split(filename)[-1].lower().split('.')[-1]
        #print(file_end)
        check = imghdr.what(filename)
        #print(check)
        if check == None:
            #print('error file! remove', filename)
            error_images+=1
            #srcfile = filename
            #dstfile = filename.replace('.'+file_end, 'error.'+file_end)
            #shutil.move(srcfile,dstfile)          #移动文件
            os.remove(filename)
        elif check!=file_end:
            srcfile = filename
            dstfile = filename.replace(file_end, check)
            # print('{} rename to {}'.format(srcfile, dstfile))
            shutil.move(srcfile,dstfile)          #移动文件
        else:
            pass
    print('error images num:', error_images)


# 获取文件大小
def getFileSize(path):
    try:
        size = os.path.getsize(path)
        return size
    except Exception as err:
        print(err)

def chk_size_wh(root_path):

    original_images = get_filelist(root_path)
    
    small_images=0
    size_th = 1024 * 100      #100Kb
    w_th = 224
    h_th = 224
    for filename in tqdm(original_images):
        b_size = getFileSize(filename)
        #print(b_size)
        if b_size<size_th:
            image=cv2.imread(filename)
            if image is None:
                os.remove(filename)   # gif opencv 不能处理
                small_images+=1
                continue
            height=image.shape[0]
            width=image.shape[1]
            if height<h_th or width<w_th:
                #print('too small file! remove', filename)
                #file_end = os.path.split(filename)[-1].lower().split('.')[-1]
                #srcfile = filename
                #dstfile = filename.replace('.'+file_end, 'small.'+file_end)
                #shutil.move(srcfile,dstfile)          #移动文件
                os.remove(filename)
                small_images+=1
        else:
            pass
    print('too small images:', small_images)


if __name__ == '__main__':

    root_path = '/media/kevin/备份/weather/fast-MPN-COV/CK6typesWeatherTestData (复件)/ImageNet'
    
    chk_error_type(root_path)
    chk_valid_jpg(root_path)
    chk_size_wh(root_path)
    remove_same_piture_by_get_md5(root_path)
    #remove_simillar_picture_by_perception_hash(root_path)


