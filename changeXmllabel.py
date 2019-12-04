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
    xmlDir=r'/DATACENTER4/ke.cao/xizang_testdata/1118/Annotations'
    
    changeLabelDict={
    'person_foreign':'person_foreign',
    'motorbike_foreign':'car_foreign',
    'car_foreign':'car_foreign',
    'SUV_foreign':'car_foreign',
    'bus_foreign':'car_foreign',
    'microbus_foreign':'car_foreign',
    'micorbus_foreign':'car_foreign',
    'pickup_foreign':'car_foreign',
    'truck_foreign':'car_foreign',
    'tanker_foreign':'car_foreign',
    'tractor_foreign':'car_foreign',
    'engineeringvan_foreign':'car_foreign',
    'tricycle_foreign':'car_foreign',
    'person':'person',
    'motorbike':'car',
    'car':'car',
    'SUV':'car',
    'bus':'car',
    'microbus':'car',
    'pickup':'car',
    'truck':'car',
    'tanker':'car',
    'tractor':'car',
    'engineeringvan':'car',
    'tricycle':'car',
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
