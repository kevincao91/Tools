#encoding=utf-8
import os
import shutil
from basicFun import FILES
if __name__=="__main__":
    kind='door_close'
    referXml="/DATACENTER5/hao.yang/dataRoom/Qin/safe/caotan/referXml/{}.xml".format(kind)
    xmlDir="/DATACENTER5/hao.yang/dataRoom/Qin/safe/caotan/labels_door/"
    imgDir="/DATACENTER5/hao.yang/dataRoom/Qin/safe/caotan/safe_door_classified_all/{}".format(kind)
    allfiles=[x for x in FILES.get_sorted_files(imgDir)]
    for file in allfiles:
        newPath=os.path.join(xmlDir,file.split('.')[0]+'.xml')
        shutil.copy(referXml,newPath)