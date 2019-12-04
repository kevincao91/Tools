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
    operators=['gs','hs','px','tsy','zxy','yy','wzx','lf','dxj']
    referDir1="/DATACENTER6/hao.yang/dataRoom/Qin/trade/labelTask_phone/labels_phone/"
    referForm=".xml"
    allRefers=[x for x in FILES.get_files(referDir1) if referForm in x]#审核为.refer形成列表
    # dirName='safe_close'
    for operator in operators:
        count=0
        # referDir2=referDir1.replace('door_close','door_open')
        sourDir="/DATACENTER6/hao.yang/dataRoom/Qin/trade/labelTask_phone/{}".format(operator)
        sourForm=".jpg"
        tarDir='/DATACENTER6/hao.yang/dataRoom/Qin/trade/labelTask_phone/abandon/'
        # tarDir=os.path.join(tarDir,operator)
        tarForm=".jpg"
        FILES.mkdir(tarDir)
        allImgs=[x for x in FILES.get_files(sourDir) if sourForm in x]
        for img in allImgs:
            if img.replace(sourForm,referForm) not in allRefers:
                sour=img.split('.')[0]+sourForm
                tar=img.split('.')[0]+tarForm
                sourPath=os.path.join(sourDir,sour)
                tarPath=os.path.join(tarDir,tar)
                try:
                    shutil.move(sourPath,tarPath)
                    count+=1
                except:
                    pass
        print(count)
        print("running time ", time.time()-start)
