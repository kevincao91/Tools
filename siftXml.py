#encoding=utf-8
# 将xml的filename和size标准化
import os,cv2
from basicFun import XML,FILES,COCO
from tqdm import tqdm
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
def regular_xml(path,filename):
    global count
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    # XML.chag_label(root,labelDict) # 修改label名称
    # root=XML.del_tag(root,names) # 删除指定label
    root=XML.save_tag(root,names) # 只保留指定label
    # root=XML.thresh_size(path,root,sizeThresh,sizeThreshNames)
    XML.write_xml(tree,path)
if __name__=="__main__":
    count=0
    xmlDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/checkout/pos_use_pos/'
    print(xmlDir)
    names=['pos_free','pos_use']    
    # names=['yellow','blue','other','security','red','gray']
    # names=['truck','oilgun','motorcycle','bus','tanker','vehicle']
    # names=['yellow','blue','other','security','red','gray','truck','oilgun','motorcycle','bus']
    # labelDict={'oilgun':'vehicle','motorcycle':'vehicle','bus':'vehicle','truck':'vehicle'}
    labelDict={'tanker':'vehicle','bus':'oilgun','truck':'oilgun'}
    sizeThresh=(60,60)
    sizeThreshNames=['clamp_on']
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]
    for xml in tqdm(allXmls):
        xmlPath=os.path.join(xmlDir,xml)
        try:
            regular_xml(xmlPath,xml.split('.')[0])
        except:
            print('{} regular_wh failed'.format(xmlPath))
            continue
    print('Totally regular wh {} xmls'.format(count))
