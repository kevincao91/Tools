import os,shutil
from basicFun import FILES,XML
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
def get_iou(box_a,box_b):
    def get_area(areaBox):
        ha=areaBox[3]-areaBox[1]
        wa=areaBox[2]-areaBox[0]
        return(ha*wa)
    int_box_a=[int(box_a['xmin']),int(box_a['ymin']),int(box_a['xmax']),int(box_a['ymax'])]
    int_box_b=[int(box_b['xmin']),int(box_b['ymin']),int(box_b['xmax']),int(box_b['ymax'])]
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
        bArea=float(get_area(int_box_b))
        return (overlapArea/(aArea+bArea-overlapArea))
def find_a_differ(labelObj,modelObjs):
    differ=0
    match=0
    for modelObj in modelObjs:
        iou=get_iou(labelObj,modelObj)
        if iou>0.8:
            match=1
            if labelObj['name']!=modelObj['name'] and labelObj['name'] not in nocareKinds :
                print(labelObj['name'])
                differ=1
                break
    return differ
def fuse(labelObj,modelObjs):
    for modelObj in modelObjs:
        iou=0.0
        if modelObj['name'] in attentionNames:
            print(labelObj,modelObj)
            iou=get_iou(labelObj,modelObj)
            print(iou)
        if iou>0.6:
            labelObj['name']=modelObj['name']
    return labelObj
modelXmlDir='/disk2/hao.yang/project/Qin/data/imgs/isle/modelxml_isle_17117_withred/'
labelXmlDir=r'/disk2/hao.yang/project/Qin/data/imgs/isle/modelxml_isle_17117_havered/'
# checkedDir='/disk2/hao.yang/project/Qin/data/xmls/checkout/complete'
attentionNames=['red']
confuseNames=['yellow','other','blue']
count=0
allChecked=[]
# allChecked=[x for x in FILES.get_sorted_files(checkedDir) if ".xml" in x]
allXmls=[x for x in FILES.get_sorted_files(modelXmlDir) if ".xml" in x and x not in allChecked]
for xml in allXmls:
    labelXmlPath=os.path.join(labelXmlDir,xml)
    modelXmlPath=os.path.join(modelXmlDir,xml)
    if os.path.exists(labelXmlPath):
        labelObjs=XML.read_objects(labelXmlPath)
        modelObjs=XML.read_objects(modelXmlPath)
        newObjs=[]
        for labelObj in labelObjs:
            if labelObj['name'] in confuseNames:
                newObjs.append(fuse(labelObj,modelObjs))
            else:
                newObjs.append(labelObj)
        tree = ET.ElementTree(file=labelXmlPath)
        root = tree.getroot()
        XML.del_all_tag(root)
        for box in newObjs:
            root=XML.add_tag(root,box)
        XML.write_xml(tree,labelXmlPath)   
# FILES.copy_files_refer_dir(imgDir,'.jpg',badDir,badDir)
