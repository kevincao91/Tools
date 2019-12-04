# encoding=utf8
import os
import shutil
from basicFun import FILES
if __name__ == "__main__":
    count=0
    referDir=r"/DATACENTER4/hao.yang/project/Qin/data/imgs/checkout/imgs_checkout_10583_divide/"
    referForm=".jpg"
    sourDir=r"/DATACENTER3/fhn/xian_data/datasets/checkout/20190704_10972/xml_checkout_10972_total/"
    sourForm=".xml"
    tarDir=r"/DATACENTER4/hao.yang/project/Qin/data/imgs/checkout/0705/"
    tarForm=sourForm
    allRefers=[x for x in FILES.list_all_files(referDir) if referForm in x]#审核为.refer形成列表
    allJpgs=[x for x in FILES.list_all_filePaths(sourDir) if sourForm in x]
    FILES.mkdir(tarDir)
    for jpgPath in allJpgs:
        if jpgPath.split('/')[-1].replace(sourForm,referForm) not in allRefers :
            shutil.copy(jpgPath,os.path.join(tarDir,jpgPath.split('/')[-1]))
            count+=1
    print("copy jpgs:",count)
