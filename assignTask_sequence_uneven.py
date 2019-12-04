#encoding=utf-8
'assign img & xml task to members'
import os
import shutil
import random
# personal lib
from basicFun import FILES
if __name__=="__main__":
    namei=0
    evenMembers=['szl','hs']
    limitMembers={'zzh':60}
    taskDir=r'/DATACENTER4/hao.yang/project/Qin/data/preProcess/removedSimilarityFrame/0706/checkout/labeling/0706_checkout_img_hand_scanner/'
    outRoot=r'/DATACENTER4/hao.yang/project/Qin/data/preProcess/removedSimilarityFrame/0706/checkout/labeling/0706_checkout_assign_hand_scanner/'
    for member in limitMembers:
        outDir=os.path.join(outRoot,member)
        FILES.mkdir(outDir)  
    for member in evenMembers:
        outDir=os.path.join(outRoot,member)
        FILES.mkdir(outDir)         
    allImgs=FILES.get_sorted_files(taskDir)
    totalImg=len(allImgs)
    assignIndex=0
    memberI=0
    memberF=0
    # Assign to Limit Members
    for img in allImgs:
        # print(memberI)
        member=list(limitMembers.keys())[memberI]
        desDir=os.path.join(outRoot,member)
        jpgPath=os.path.join(taskDir,img)
        desJpg=os.path.join(desDir,img)
        # copy file
        shutil.move(jpgPath,desJpg)
        assignIndex+=1
        memberF+=1
        if memberF>=limitMembers[member]:
            memberF=0
            memberI+=1
        if memberI==len(limitMembers):
            memberI=0
            remainImg=totalImg-assignIndex
            break
    # 每人大概分配的数量
    perAmount=remainImg/len(evenMembers)
    # 可能会有分不匀的情况
    redundant=remainImg%len(evenMembers)
    print('{}*{}+{}=?{}'.format(perAmount,len(evenMembers),redundant,len(allImgs)))
    assignCount=0  
    memberAmount=perAmount   
    for i,img in enumerate(allImgs):
        if i<assignIndex:
            continue
        if assignCount<memberAmount:
            desDir=os.path.join(outRoot,evenMembers[memberI])
            srcPath=os.path.join(taskDir,img)
            desPath=os.path.join(desDir,img)
            shutil.move(srcPath,desPath)
            assignCount+=1
        else:
            print('member:{} amount:{}'.format(evenMembers[memberI],assignCount))
            assignCount=0
            memberI+=1
            # 将未分均匀的部分挨个添加到随机的成员中
            if redundant>0:
                memberAmount=perAmount+1
                redundant-=1
            else:
                memberAmount=perAmount
    print('member:{} amount:{}'.format(evenMembers[memberI],assignCount))
    # Assign to evenMembers
    # for i,img in enumerate(allImgs):
    #     # print(memberI)
    #     if i <assignIndex:
    #         continue
    #     remainImg=totalImg-assignIndex
    #     remainMembers=
    #     member=members[memberI]
    #     if member in limitMembers.keys():
    #         desDir=os.path.join(outRoot,member)
    #         jpgPath=os.path.join(taskDir,img)
    #         desJpg=os.path.join(desDir,img)
    #         # copy file
    #         # shutil.copy(jpgPath,desJpg)
    #         assignIndex+=1
    #         memberF+=1
    #         if memberF>=limitMembers[member]:
    #             memberF=0
    #             memberI+=1    