# coding:utf-8
import os
import glob
import random
'''
    为数据集生成对应的txt文件
'''

train_txt_path = './testdata/1107/train.txt'
train_dir = '/media/kevin/娱乐/weather_database/sysdata/rains/train'

trainval_txt_path = './testdata/1107/trainval.txt'
trainval_dir = './testdata/1101/trainval/'

valid_txt_path = './testdata/1107/valid.txt'
valid_dir = '/media/kevin/娱乐/weather_database/sysdata/rains/validation'

test_txt_path = './testdata/1107/test.txt'
test_dir = './testdata/1101/test/'

# 文件夹内有子文件夹，获取的路径是文件名和路径
def gen_txt_2(txt_path, img_dir):
    f = open(txt_path, 'w')
    
    for root, dirs, files in os.walk(img_dir):
        print(root, dirs)

        for dir_ in dirs:
            imgs_list = glob.glob(os.path.join(root, dir_, '*.jpg'))
            
            random.seed(666)
            random.shuffle(imgs_list)
            imgs_num = len(imgs_list)
            
            label = root[-1]

            for i in range(imgs_num):
                img_path = imgs_list[i]
                line = img_path[47:] + ' ' + label + '\n'
                f.write(line)

    f.close()
    
    

# 文件夹内没有子文件夹，获取的路径是文件名
def gen_txt(txt_path, img_dir):
    f = open(txt_path, 'w')
    
    img_list = os.listdir(img_dir)                    # 获取类别文件夹下所有jpg图片的路径
    for i in range(len(img_list)):
        if not img_list[i].endswith('jpg'):         # 若不是jpg文件，跳过
            continue
        label = img_list[i].split('_')[0]
        img_path = img_list[i]
        if label=='sunny':
            label = 0
        if label=='cloudy':
            label = 1
        line = img_path + ' ' + str(label) + '\n'
        f.write(line)
    f.close()


if __name__ == '__main__':

    gen_txt_2(train_txt_path, train_dir)
    gen_txt_2(valid_txt_path, valid_dir)

'''
    gen_txt(train_txt_path, train_dir)
    gen_txt(trainval_txt_path, trainval_dir)
    gen_txt(valid_txt_path, valid_dir)
    gen_txt(test_txt_path, test_dir)
'''
