#encoding=utf-8
# 将xml的filename和size标准化
import os,cv2,sys
from basicFun import XML,FILES,COCO
from tqdm import tqdm
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
def regular_xml(path,changeLabelDict):
    global count
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    XML.chag_label(root,changeLabelDict,tag="object")
    XML.write_xml(tree,path)
    
if __name__=="__main__":
    count=0
    xmlDir=r'/home/kevin/桌面/ck'
    
    changeLabelDict={
    'car':'car',
    'bus':'car',
    'van':'car',
    'others':'car',
    'security':'other',
    'blue':'blue',
    'other':'other',
    'door_open':'door_open',
    }
    print(xmlDir)
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]
    for xml in tqdm(allXmls):
        xmlPath=os.path.join(xmlDir,xml)
        try:
            regular_xml(xmlPath,changeLabelDict)
            count += 1
        except:
            print('{} change label failed'.format(xmlPath))
            continue
    print('Totally change label {} xmls'.format(count))
