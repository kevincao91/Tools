#encoding=utf-8
# 
import os,cv2,sys
from basicFun import XML,FILES
from tqdm import tqdm
import numpy as np
import shutil



def analyze_xml(path):

    objs = XML.read_objects(path)
    #print(objs)
    
    img_weight = 0
    for obj in objs:
        name = obj['name']
        if name in obw:
            img_weight+=obw[name]
        else:
            print(path)
            exit()
    return img_weight
    
if __name__=="__main__":
    global obw
    '''
    ob_num={
    'person':70000,
    'motorbike':16000,
    'car':213000,
    'bus':20000,
    'truck':69000,
    'microbus':40000,
    'pickup':15000,
    'SUV':100000,
    'tanker':8000,
    'tractor':6000,
    'engineeringvan':2000,
    'tricycle':4000,
    }
    total_num=563000
    keep_img_num = 10000
    obw={
    'person':total_num/ob_num['person'],
    'motorbike':total_num/ob_num['motorbike'],
    'car':total_num/ob_num['car'],
    'bus':total_num/ob_num['bus'],
    'truck':total_num/ob_num['truck'],
    'microbus':total_num/ob_num['microbus'],
    'pickup':total_num/ob_num['pickup'],
    'SUV':total_num/ob_num['SUV'],
    'tanker':total_num/ob_num['tanker'],
    'tractor':total_num/ob_num['tractor'],
    'engineeringvan':total_num/ob_num['engineeringvan'],
    'tricycle':total_num/ob_num['tricycle'],
    }
    '''
    
    ob_num={
    'person_foreign':12600,
    'motorbike_foreign':1992,
    'car_foreign':2854,
    'bus_foreign':1241,
    'truck_foreign':1443,
    'microbus_foreign':861,
    'pickup_foreign':375,
    'SUV_foreign':690,
    'tanker_foreign':106,
    'tractor_foreign':363,
    'engineeringvan_foreign':137,
    'tricycle_foreign':693,
    }
    total_num=23355
    keep_img_num = 3000
    obw={
    'person_foreign':total_num/ob_num['person_foreign'],
    'motorbike_foreign':total_num/ob_num['motorbike_foreign'],
    'car_foreign':total_num/ob_num['car_foreign'],
    'bus_foreign':total_num/ob_num['bus_foreign'],
    'truck_foreign':total_num/ob_num['truck_foreign'],
    'microbus_foreign':total_num/ob_num['microbus_foreign'],
    'pickup_foreign':total_num/ob_num['pickup_foreign'],
    'SUV_foreign':total_num/ob_num['SUV_foreign'],
    'tanker_foreign':total_num/ob_num['tanker_foreign'],
    'tractor_foreign':total_num/ob_num['tractor_foreign'],
    'engineeringvan_foreign':total_num/ob_num['engineeringvan_foreign'],
    'tricycle_foreign':total_num/ob_num['tricycle_foreign'],
    }
    
    imgDir=r'/media/kevin/DataSet/xizang_database/label_data/xizang_foreign_road_1125/JPEGImages'
    xmlDir=r'/media/kevin/DataSet/xizang_database/label_data/xizang_foreign_road_1125/Annotations'
    toimgDir=r'/media/kevin/DataSet/xizang_database/label_data/JPEGImages'
    toxmlDir=r'/media/kevin/DataSet/xizang_database/label_data/Annotations'
    FILES.mkdir(toimgDir)
    FILES.mkdir(toxmlDir)
    
    print(xmlDir)
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]

    weights = []
    for xml in tqdm(allXmls):
        xmlPath=os.path.join(xmlDir,xml)

        img_weight = analyze_xml(xmlPath)
        weights.append((img_weight, xmlPath))
        
    weights.sort(reverse = True)
    #print(weights[:20])
    exit()
    for weight_ in tqdm(weights[:keep_img_num]):
        xmlPath = weight_[1]
        xml = os.path.split(xmlPath)[-1]
        toxmlPath = os.path.join(toxmlDir,xml)
        shutil.copy(xmlPath,toxmlPath)
        imgPath=os.path.join(imgDir,xml.replace('.xml','.jpg'))
        img = os.path.split(imgPath)[-1]
        toimgPath = os.path.join(toimgDir,img)
        shutil.copy(imgPath,toimgPath)
    print('Totally mv {} data'.format(keep_img_num))
    

    
