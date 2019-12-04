#encoding=utf-8
# Element.remove()
# Element.findall() finds only elements with a tag which are direct children of the current element
import os
from basicFun import XML
from basicFun import FILES
import shutil
import time
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
def add_box(path,boxes):
    # print(path)
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    for bndbox in boxes:
        root=XML.add_tag(root,bndbox)
    XML.write_xml(tree,path) 
    # print('ok')
def trans_box(Box,augValue_xmin,augValue_ymin,augValue_xmax,augValue_ymax):
    box=[0,0,0,0,0]
    box[0]=Box[0]
    w=int(Box[3])-int(Box[1])
    h=int(Box[4])-int(Box[2])
    box[1]=str(int(int(Box[1])+w*augValue_xmin))
    box[2]=str(int(int(Box[2])+h*augValue_ymin))
    box[3]=str(int(int(Box[3])-w*augValue_xmax))
    box[4]=str(int(int(Box[4])-h*augValue_ymax))
    return box
def check_overlap(safebox,BBOXES):
    for i in range(len(BBOXES)):
        if BBOXES[i][0] not in augNameList:#非保险柜box
            overlapRate=get_overlapRate(safebox,BBOXES[i])
            if overlapRate>0.3:
                return 0
    return 1
def get_overlapRate(box_a,box_b):
    int_box_a=[int(box_a[1]),int(box_a[2]),int(box_a[3]),int(box_a[4])]
    int_box_b=[int(box_b[1]),int(box_b[2]),int(box_b[3]),int(box_b[4])]
    # int_box=[xmin,ymin,xmax,ymax]
    # 设a为基准
    box_share=[0,0,0,0]
    # x
    # 若右交
    if int_box_b[0]<int_box_a[2]:
        box_share[0]=max(int_box_a[0],int_box_b[0])
    # 若左交
        if int_box_a[0]<int_box_b[2]:
            box_share[2]=min(int_box_a[2],int_box_b[2])
        else:
            return 0
    else:
        return 0
    # y
    # 若右交
    if int_box_b[1]<int_box_a[3]:
        box_share[1]=max(int_box_a[1],int_box_b[1])
    # 若左交
        if int_box_a[1]<int_box_b[3]:
            box_share[3]=min(int_box_a[3],int_box_b[3])
        else:
            return 0
    else:
        return 0
    if box_share:
        overlapArea=float(get_area(box_share))
        aArea=float(get_area(int_box_a))
        return (overlapArea/aArea)
def get_area(areaBox):
    ha=areaBox[3]-areaBox[1]
    wa=areaBox[2]-areaBox[0]
    return(ha*wa)
if __name__=="__main__":
    time_sta=time.time()
    augNameList=['close','cover','open']
    xmlDir=r"/DATACENTER2/yh/detectron/caffe2/train/safebox/faster_voc/11469/xml_1713"
    tarDir=r"/DATACENTER2/yh/detectron/caffe2/train/safebox/faster_voc/11469/xml_1713_aug"
    FILES.mkdir(tarDir)
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]
    cur=0
    bgn=800 #包含
    end=1900 #包含
    for xml in allXmls:
        cur+=1
        # print(cur) #第cur个文件
        if cur>=bgn and cur<=end:
            xmlPath=xmlDir+'/'+xml
            tarXmlPath=tarDir+'/'+xml
            shutil.copy(xmlPath,tarXmlPath)
            BBOXES=XML.read_object(xmlPath)
            for augRate_xmin in range(0,5):
                augValue_xmin=augRate_xmin*0.02
                for augRate_xmax in range(0,5):
                    augValue_xmax=augRate_xmax*0.02
                    for augRate_ymin in range(0,5):
                        augValue_ymin=augRate_ymin*0.02
                        for augRate_ymax in range(0,5):
                            augValue_ymax=augRate_ymax*0.02
                            if augRate_xmin+augRate_xmax+augRate_ymin+augRate_ymax!=0:
                                bboxes=[]
                                for i in range(len(BBOXES)):
                                    if BBOXES[i][0] in augNameList and check_overlap(BBOXES[i],BBOXES):
                                        bboxes.append(trans_box(BBOXES[i],augValue_xmin,augValue_ymin,augValue_xmax,augValue_ymax))
                                try:
                                    add_box(tarXmlPath,bboxes)
                                except:
                                    continue
    print(time.time()-time_sta)



