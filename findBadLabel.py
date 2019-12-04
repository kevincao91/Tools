#coding=utf-8
import os,shutil,copy
from basicFun import FILES,XML
from tqdm import tqdm
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
        if iou>0.6:
            match=1
            if labelObj['name']!=modelObj['name'] and labelObj['name'] not in nocareKinds :
                print(labelObj['name'])
                differ=1
                break
    return differ
def combine(modelObjs,labelObjs):
    # print(len(labelObjs))
    newObjs=[]
    differ=0
    restLabels=copy.deepcopy(labelObjs)
    for modelObj in modelObjs:
        if modelObj['name'] in nocareKinds:
            continue
        maxiou=0
        matchLabel=copy.deepcopy(modelObj)
        for labelObj in labelObjs:
            iou=get_iou(modelObj,labelObj)
            if iou>maxiou:
                matchLabel=labelObj
                maxiou=iou
        if maxiou>0.5:
            if modelObj['name']!=matchLabel['name']  and labelObj['name'] not in nocareKinds:
                differ=1
                if matchLabel in restLabels:
                    restLabels.remove(matchLabel)
                matchLabel['name']=modelObj['name']
            else:
                if matchLabel in restLabels:
                    restLabels.remove(matchLabel)
        else:
            if modelObj['name'] not in bigNames:
                matchLabel=copy.deepcopy(modelObj)
                # differ=1
        newObjs.append(matchLabel)
    for labelObj in restLabels:
        newObjs.append(labelObj)
    return differ,newObjs
imgDir=r'/DATACENTER4/hao.yang/project/Qin/data/imgs/safe/safe_FMXX_img/'
# modelXmlDir=imgDir[:-1]+'_modelxml_baseline4'
modelXmlDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/safe/modelXml_safe_FMXX/'
labelXmlDir=r'/DATACENTER4/hao.yang/project/Qin/data/xmls/safe/safe_FMXX_22983_total/'
badDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/safe/bad_safe_FMXX/'
checkedDir='/'
FILES.rm_mkdir(badDir)
nocareKinds=['cashbox_close','cashbox_open','safe_hide','jug']
bigNames=[]
# bigNames不可能有漏标，如果漏掉，必然是故意的，所以不算错误
count=0
allChecked=[x for x in FILES.get_sorted_files(checkedDir) if ".xml" in x]
if allChecked:
    allXmls=[x for x in FILES.get_sorted_files(labelXmlDir) if ".xml" in x and x not in allChecked]
else:
    allXmls=[x for x in FILES.get_sorted_files(modelXmlDir) if ".xml" in x ]
for xml in tqdm(allXmls):
    labelXmlPath=os.path.join(labelXmlDir,xml)
    modelXmlPath=os.path.join(modelXmlDir,xml)
    if os.path.exists(labelXmlPath):
        modelObjs=XML.read_objects(modelXmlPath)
        labelObjs=XML.read_objects(labelXmlPath)
        differ=0
        differ,newObjs=combine(modelObjs,labelObjs)
        if differ:
            badXmlPath=os.path.join(badDir,xml)
            shutil.copy(labelXmlPath,badXmlPath)
            # tree = ET.ElementTree(file=badXmlPath)
            # root = tree.getroot()   
            # root=XML.del_all_tag(root)
            # for boj in newObjs:
            #     root=XML.add_tag(root,boj)
            # XML.write_xml(tree,badXmlPath)  
        count+=differ
print(count)
        # for modelObj in modelObjs:
        #     newObjs.append( find_a_differ(modelObj,labelObjs):
        #         differ=1
        #         break
        # if differ:
        #     count+=1
        #     badXmlPath=os.path.join(badDir,xml)
        #     shutil.copy(modelXmlPath,badXmlPath)
FILES.copy_files_refer_dir(imgDir,'.jpg',badDir,badDir)
