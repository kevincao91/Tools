#encoding=utf8
#由于文件夹中只标注了部分refer，因此按照xx.refer复制已标注的xx.jpg和xx.refer到新的文件夹
#单文件夹
import os
import shutil
import time
from basicFun import FILES
if __name__=="__main__":
    count=0    
    start=time.time()
    referDir=r'/DATACENTER4/hao.yang/project/Qin/data/preProcess/removedSimilarityFrame/0706/checkout/labeling/0706_checkout_assign_person/lf/'
    referForm=".jpg"
    sourDir=r"/DATACENTER4/hao.yang/project/Qin/data/preProcess/removedSimilarityFrame/0706/checkout/labeling/0706_checkout_person/"
    sourForm=".xml"
    tarDir=referDir
    tarForm=sourForm
    FILES.mkdir(tarDir)
    print('Refering {}'.format(referDir))
    allRefers=[x for x in FILES.list_all_files(referDir) if referForm in x]#审核为.refer形成列表
    for refer in allRefers:
        sour=refer.split('.')[0]+sourForm
        tar=refer.split('.')[0]+tarForm
        sourPath=os.path.join(sourDir,sour)
        tarPath=os.path.join(tarDir,tar)
        try:
            shutil.copy(sourPath,tarPath)
            count+=1
        except:
            # print('No file: {}'.format(sourPath))
            pass
    print(count)
    print("running time ", time.time()-start)
