#encoding=utf-8
# 将xml的filename和size标准化
import os, sys
from basicFun import XML
from tqdm import tqdm
import shutil
import glob
    
root_dir = '/media/kevin/娱乐/xizang_database/label_data/JPEGImages (未去重)'
target_dir = '/media/kevin/娱乐/xizang_database/label_data/JPEGImages (未去重)'
    

def rename_newidx():

    for root, dirs, files in os.walk(img_root_dir):
        imgs_list = glob.glob(os.path.join(root, '*.jpg'))
        num_max = len(imgs_list)
        break

    print(imgs_list)
  
    start_num = 4150  
    for idx, img in tqdm(enumerate(imgs_list)):
        img = img.split('/')[-1]
        imgPath=os.path.join(img_root_dir, img)

        newimg = str(idx+start_num).zfill(4) + '.jpg'
        newimgPath=os.path.join(img_target_dir, newimg)
        shutil.copy(imgPath,newimgPath)
        # print('move ok')

    print('Totally rename {} files'.format(idx+1))
    
def rename_addlabel():

    for root, dirs, files in os.walk(root_dir):
        files_list = glob.glob(os.path.join(root, '*.*'))
        num_max = len(files_list)
        break

    # print(imgs_list)
    count = 0
    add_label = 'xizang_'  
    for file_path in tqdm(files_list):
        file_name = file_path.split('/')[-1]
        new_file_name = add_label + file_name
        new_file_path = os.path.join(target_dir, new_file_name)
        shutil.move(file_path,new_file_path)
        count += 1
        # print('move ok')

    print('Totally rename {} files'.format(count))

def rename_dellabel():

    for root, dirs, files in os.walk(root_dir):
        files_list = glob.glob(os.path.join(root, '*.*'))
        num_max = len(files_list)
        break

    # print(imgs_list)
    count = 0
    del_label = 'xizang_'  
    for file_path in tqdm(files_list):
        file_name = file_path.split('/')[-1]
        new_file_name = file_name.replace(del_label, "")
        new_file_path = os.path.join(target_dir, new_file_name)
        shutil.move(file_path,new_file_path)
        count += 1
        # print('move ok')

    print('Totally rename {} files'.format(count))


if __name__=="__main__":

    rename_addlabel()


