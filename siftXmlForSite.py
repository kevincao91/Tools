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
    if os.path.exists(path):
        tree = ET.ElementTree(file=path)
        root = tree.getroot()
        # XML.chag_label(root,labelDict) # 修改label名称
        # root=XML.del_tag(root,names) # 删除指定label
        # root=XML.save_tag(root,names) # 只保留指定label
        XML.thresh_size(root,width,sizeThreshDict)
        XML.write_xml(tree,path)
if __name__=="__main__":
    imgDir='/DATACENTER4/hao.yang/project/Qin/data/imgs/unload/img_unload_38212_divided/'
    allJpgs=[x for x in FILES.list_all_filePaths(imgDir) if '.jpg' in x]
    xmlDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/unload/xml_unload_38212_rdclamp_rmtube/'
    print(xmlDir)
    names=['clamp_on']    
    # names=['yellow','blue','other','security','red','gray']
    # names=['truck','oilgun','motorcycle','bus','tanker','vehicle']
    # names=['yellow','blue','other','security','red','gray','truck','oilgun','motorcycle','bus']
    # labelDict={'oilgun':'vehicle','motorcycle':'vehicle','bus':'vehicle','truck':'vehicle'}
    # labelDict={'motorcycle':'oilgun','bus':'oilgun','truck':'oilgun'}
    sizeThresh=(400,1000)
    sizeThreshDict={'clamp_on':sizeThresh}
    count=0
    for jpgPath in tqdm(allJpgs):
        if 'xiwan' in jpgPath:
            jpg=jpgPath.split('/')[-1]
            xmlPath=os.path.join(xmlDir,jpg.replace('.jpg','.xml'))
            image=cv2.imread(jpgPath)
            width=image.shape[1]
            regular_xml(xmlPath,jpg.split('.')[0])
            # try:
            #     regular_xml(xmlPath,jpg.split('.')[0])
            # except:
            #     print('{} regular_wh failed'.format(xmlPath))
                # continue
    print('Totally regular wh {} xmls'.format(count))
