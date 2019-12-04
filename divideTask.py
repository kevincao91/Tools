#encoding=utf-8
'assign img task to members as sequence'
import os
import shutil
import random
# personal lib
from basicFun import FILES
if __name__=="__main__":
    namei=0
    preTitle='isle5_phase1_FengShi'
    members=['p1','p2','p3','p4']
    random.shuffle(members)
    jpgDir='/disk2/hao.yang/project/Qin/data/isle/FengShi/isle5_phase1_img/'
    xmlDir='/disk2/hao.yang/project/Qin/data/isle/FengShi/isle5_phase1_img_autoperson/'
    outRoot='/disk2/hao.yang/project/Qin/data/isle/FengShi/labelAssign/{}_assign/'.format(preTitle)
    FILES.rm_mkdir(outRoot)
    allImgs=FILES.get_sorted_files(jpgDir)
    # 每人大概分配的数量
    perAmount=int(len(allImgs)/len(members))
    # 可能会有分不匀的情况
    redundant=len(allImgs)%len(members)
    print('{}*{}+{}=?{}'.format(perAmount,len(members),redundant,len(allImgs)))
    assignCount=0
    for member in members:
        outDir=os.path.join(outRoot,'{}_{}'.format(preTitle,member))
        FILES.rm_mkdir(outDir)  
    memberAmount=perAmount
    for img in allImgs:
        if assignCount<memberAmount:
            # print(members[namei])
            desDir=os.path.join(outRoot,'{}_{}/{}_{}_img'.format(preTitle,members[namei],preTitle,members[namei]))
            FILES.mkdir(desDir)
            srcPath=os.path.join(jpgDir,img)
            desPath=os.path.join(desDir,img)
            shutil.copy(srcPath,desPath)
            desDir=os.path.join(outRoot,'{}_{}/{}_{}_xml'.format(preTitle,members[namei],preTitle,members[namei]))
            FILES.mkdir(desDir)
            srcPath=os.path.join(xmlDir,img.replace('.jpg','.xml'))
            if os.path.exists(srcPath):
                desPath=os.path.join(desDir,img.replace('.jpg','.xml'))
                shutil.copy(srcPath,desPath)
            assignCount+=1
        else:
            print('member:{} amount:{}'.format(members[namei],assignCount))
            assignCount=0
            namei+=1
            print('redundant={},memberAmount={},perAmount={}'.format(redundant,memberAmount,perAmount))
            # 将未分均匀的部分挨个添加到随机的成员中
            if redundant>0:
                memberAmount=perAmount+1
                redundant-=1
            else:
                memberAmount=perAmount
            desDir=os.path.join(outRoot,'{}_{}/{}_{}_img'.format(preTitle,members[namei],preTitle,members[namei]))
            FILES.mkdir(desDir)
            srcPath=os.path.join(jpgDir,img)
            desPath=os.path.join(desDir,img)
            shutil.copy(srcPath,desPath)
            desDir=os.path.join(outRoot,'{}_{}/{}_{}_xml'.format(preTitle,members[namei],preTitle,members[namei]))
            FILES.mkdir(desDir)
            srcPath=os.path.join(xmlDir,img.replace('.jpg','.xml'))
            if os.path.exists(srcPath):
                desPath=os.path.join(desDir,img.replace('.jpg','.xml'))
                shutil.copy(srcPath,desPath)
            assignCount+=1
