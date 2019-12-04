#encoding=utf-8
# 将xml的filename和size标准化
import os,cv2,sys
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
    XML.chk_label(root,sizeThreshDict)
    XML.chag_size(root,filename,width,height)
    XML.chag_filename(root,filename)
    XML.thresh_size(root,width,sizeThreshDict)
    XML.write_xml(tree,path)
    
if __name__=="__main__":
    count=0
    imgDir=r'/media/kevin/娱乐/xizang_database/testdata/1125/JPEGImages'
    xmlDir=r'/media/kevin/娱乐/xizang_database/testdata/1125/all_Annotations_no_change_label'
    
    personThresh=(20,60)
    vehicleThresh=(50,50)
    sizeThreshDict={
    'person_foreign':personThresh,
    'motorbike_foreign':vehicleThresh,
    'car_foreign':vehicleThresh,
    'SUV_foreign':vehicleThresh,
    'bus_foreign':vehicleThresh,
    'microbus_foreign':vehicleThresh,
    'pickup_foreign':vehicleThresh,
    'truck_foreign':vehicleThresh,
    'tanker_foreign':vehicleThresh,
    'tractor_foreign':vehicleThresh,
    'engineeringvan_foreign':vehicleThresh,
    'tricycle_foreign':vehicleThresh,
    'person':personThresh,
    'motorbike':vehicleThresh,
    'car':vehicleThresh,
    'SUV':vehicleThresh,
    'bus':vehicleThresh,
    'microbus':vehicleThresh,
    'pickup':vehicleThresh,
    'truck':vehicleThresh,
    'tanker':vehicleThresh,
    'tractor':vehicleThresh,
    'engineeringvan':vehicleThresh,
    'tricycle':vehicleThresh,
    }
    print(xmlDir)
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]
    for xml in tqdm(allXmls):
        xmlPath=os.path.join(xmlDir,xml)
        imgPath=os.path.join(imgDir,xml.replace('.xml','.jpg'))
        if not os.path.exists(imgPath):
           #os.remove(xmlPath)
           print('jpg file not exists, so remove {}'.format(xmlPath))
           continue
        image=cv2.imread(imgPath)
        height=image.shape[0]
        width=image.shape[1]
        try:
            regular_xml(xmlPath,xml.split('.')[0])
            count += 1
        except:
            print('{} regular failed'.format(xmlPath))
            continue
    print('Totally regular {} xmls'.format(count))
