# coding: utf-8
"""
    将原始数据集进行划分成训练集、验证集和测试集或整体成为测试集
"""
import os
import glob

'''
root_dir = '/DATACENTER2/ke.cao/NofE/test_data'
sence_list = ['all', 'cloudy', 'rainy', 'sunny', 'night']
'''


root_dir = '/media/kevin/娱乐/xizang_database/testdata/1125'
sence_list = ['',]


def find_all_files(sence, is_trin=True):
    if is_trin:
        xml_dir = os.path.join(root_dir, 'train_%s'%sence)
    else:
        xml_dir = os.path.join(root_dir, 'val_%s'%sence)
    
    if not os.path.exists(xml_dir):
        print('path %s no exists!'%xml_dir)
        exit()
    else:
        print(xml_dir)
    
    xml_file_path_list = glob.glob(os.path.join(xml_dir, '*.xml'))
    xml_num = len(xml_file_path_list)
    print('find %d xml file' % xml_num)
    return xml_file_path_list


def make_file(file_path_list, sence, is_train=True):

    if is_train:
        txt_path = os.path.join(root_dir, 'ImageSets', 'Main', 'train_%s.txt'%sence)
        with open(txt_path, 'w', encoding='UTF-8') as f:
            for file_path in file_path_list: 
                xml_name=os.path.basename(file_path)
                img_path=xml_name.replace('.xml','\n')
                f.write(img_path)
    else:
        txt_path = os.path.join(root_dir, 'ImageSets', 'Main', 'val_%s.txt'%sence)
        with open(txt_path, 'w', encoding='UTF-8') as f:
            for file_path in file_path_list: 
                xml_name=os.path.basename(file_path)
                img_path=xml_name.replace('.xml','\n')
                f.write(img_path)

    print('write file:{} <=={}lines'.format(txt_path, len(file_path_list)))


if __name__ == '__main__':
    for sence in sence_list:
        print('sence:', sence)
        # train
        xml_file_path_list = find_all_files(sence, True)
        make_file(xml_file_path_list, sence, True)
        # val
        xml_file_path_list = find_all_files(sence, False)
        make_file(xml_file_path_list, sence, False)
        
    print('Done!')
        

