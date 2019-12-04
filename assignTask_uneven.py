#encoding=utf-8
'assign img & xml task to members'
import os
import shutil
import random
# personal lib
from basicFun import FILES
if __name__=="__main__":
    namei=0
    members=['ph','xgt','yxy','zt','hyd','hjc']
    membersLimits={'ph':267,'xgt':318,'yxy':360,'zt':259,'hyd':276,'hjc':413}
    taskImg=r'E:\factory\voc\helmet_img'
    taskXml=r'E:\factory\voc\labeled_xml_lackHel\xml'
    outRoot=r'E:\factory\voc\labeled_xml_lackHel_assignTask'
    for member in members:
        outDir=outRoot+'/'+member
        FILES.rm_mkdir(outDir)
        FILES.mkdir(outDir+'/img')
        FILES.mkdir(outDir+'/xml')        
    allXmls=FILES.get_sorted_files(taskXml)
    random.shuffle(allXmls)
    memberI=0
    memberF=0
    for xml in allXmls:
        print(memberI)
        member=members[memberI]
        desDir=outRoot+'/'+member
        xmlPath=taskXml+'/'+xml
        desXml=desDir+'/xml/'+xml
        jpg=xml.split('.')[0]+'.jpg'
        jpgPath=taskImg+'/'+jpg
        desJpg=desDir+'/img/'+jpg
        # copy file
        shutil.copy(xmlPath,desXml)
        shutil.copy(jpgPath,desJpg)
        memberF+=1
        if memberF>=membersLimits[member]:
            memberF=0
            memberI+=1
