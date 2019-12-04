#encoding=utf-8
'assign img task to members as sequence'
import os
import shutil
import random
# personal lib
from basicFun import FILES
if __name__=="__main__":
    namei=0
    members=['SZL', 'SH', 'LH', 'PH','CK','DXJ','FHN','GFH','GS','HJC','HS','HYD','LF','PX','QJJ','SWL','TSY','WZX','XGT','YXY','YY','ZSH','ZT','ZXY','ZZH']
    taskDir='/media/kevin/办公/yichang/国外监控_sample_images'
    xmlDir='/media/kevin/办公/yichang/国外监控_sample_images_outputs/xml'
    outRoot=taskDir+'_todo'
    FILES.mkdir(outRoot)
    allImgs=FILES.get_sorted_files(taskDir)
    # 每人大概分配的数量
    perAmount=int(len(allImgs)/len(members))
    # 可能会有分不匀的情况
    redundant=len(allImgs)%len(members)
    print('{}*{}+{}=?{}'.format(perAmount,len(members),redundant,len(allImgs)))
    assignCount=0
    for member in members:
        outDir=os.path.join(outRoot,member)
        FILES.mkdir(outDir)  
    memberAmount=perAmount
    for img in allImgs:
        if assignCount<memberAmount:
            # print(members[namei])
            desDir=os.path.join(outRoot,members[namei])
            # jpg move
            srcPath=os.path.join(taskDir,img)
            desPath=os.path.join(desDir,img)
            shutil.copy(srcPath,desPath)
            # xml move
            xml=str(img.split('.')[0])+'.xml'
            srcPath=os.path.join(xmlDir,xml)
            desPath=os.path.join(desDir,xml)
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
            desDir=os.path.join(outRoot,members[namei])
            # jpg move
            srcPath=os.path.join(taskDir,img)
            desPath=os.path.join(desDir,img)
            shutil.copy(srcPath,desPath)
            # xml move
            xml=str(img.split('.')[0])+'.xml'
            srcPath=os.path.join(xmlDir,xml)
            desPath=os.path.join(desDir,xml)
            shutil.copy(srcPath,desPath)
            assignCount+=1
    # print('member:{} amount:{}'.format(members[namei],assignCount))
    for member in members:
        outDir=outRoot+'/'+member
        # FILES.shutil_by_refer(outDir,'.img','.jpg',taskDir,outDir)
