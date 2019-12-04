#encoding=utf-8
'assign img & xml task to members'
import os
import shutil
import random
# personal lib
from basicFun import FILES
if __name__=="__main__":
    namei=0
    members=['hs','yy','wzx','lf','dxj','zzh']
    taskImg=r'/disk3/hao.yang/project/Qin/dataRoom/XiWan/safe/img/'
    taskXml=r'/disk3/hao.yang/project/Qin/dataRoom/XiWan/safe/xml/'
    outRoot=r'/disk3/hao.yang/project/Qin/dataRoom/XiWan/safe/labelTaskAssign_safe_XiWan/'
    FILES.rm_mkdir(outRoot) 
    for member in members:
        outDir=os.path.join(outRoot,member)
        FILES.mkdir(outDir)        
    allXmls=FILES.get_sorted_files(taskXml)
    for xml in [x for x in allXmls if 'xml' in x]:
        desDir=os.path.join(outRoot,members[namei])
        xmlPath=os.path.join(taskXml,xml)
        desXml=os.path.join(desDir,xml)
        # copy file
        shutil.copy(xmlPath,desXml)
        namei+=1
        if namei==len(members):
            namei=0
            # disorder members list to increase randomness
            random.shuffle(members)
    for member in members:
        outDir=os.path.join(outRoot,member)
        FILES.shutil_by_refer(outDir,'.xml','.jpg',taskImg,outDir)
