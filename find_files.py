# coding=utf-8


import os
from tqdm import tqdm
import shutil


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


    file_list = getFiles("/media/kevin/DataSet/xizang_database/youtube/sample_videos_outputs_day", '.xml')  # =>查找以.mp4结尾的文件
    outPath="/media/kevin/DataSet/xizang_database/youtube/my_label_xml"
    if not os.path.exists(outPath):
        os.mkdir(outPath)
    
    for file_ in tqdm(file_list):
        tofile = os.path.join(outPath, file_.split('/')[-1])
        #print(file_)
        #print(tofile)
        shutil.copy(file_,tofile)
    print('over!\n')



