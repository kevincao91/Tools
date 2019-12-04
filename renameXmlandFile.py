#encoding=utf-8
# 将xml的filename和size标准化
import os, sys
from basicFun import XML
from tqdm import tqdm
import shutil
import glob
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
    

def regular_xml(newxmlPath,img,newimg):
    print(newxmlPath,xml,newxml)
    
    
    tree = ET.ElementTree(file=newxmlPath)
    root = tree.getroot()

    for obj in root.findall('filename'):
        print(obj.text)
        obj.text= newimg
        
    for obj in root.findall('path'):
        print(obj.text)
        obj.text= obj.text.replace(img, newimg)
        
    XML.write_xml(tree,newxmlPath)
    
    
if __name__=="__main__":
    count=0

    img_root_dir = '/media/kevin/娱乐/xizang_database/testdata/1115/JPEGImages'
    xml_root_dir = '/media/kevin/娱乐/xizang_database/testdata/1115/Annotations'
    img_target_dir = '/media/kevin/娱乐/xizang_database/testdata/1115/img'
    xml_target_dir = '/media/kevin/娱乐/xizang_database/testdata/1115/xml'

    for root, dirs, files in os.walk(img_root_dir):
        imgs_list = glob.glob(os.path.join(root, '*.jpg'))
        num_max = len(imgs_list)
        break

    print(imgs_list)
    
  
    for idx, img in tqdm(enumerate(imgs_list)):
        img = img.split('/')[-1]
        xml = img.replace('.jpg','.xml')
        imgPath=os.path.join(img_root_dir, img)
        xmlPath=os.path.join(xml_root_dir, xml)

        if not os.path.exists(xmlPath):
           print(xmlPath, 'not exists')
           continue
        newimg = 'xizang_' + str(idx).zfill(4) + '.jpg'
        newxml = 'xizang_' + str(idx).zfill(4) + '.xml'
        newimgPath=os.path.join(img_target_dir, newimg)
        newxmlPath=os.path.join(xml_target_dir, newxml)
        shutil.copy(imgPath,newimgPath)
        shutil.copy(xmlPath,newxmlPath)
        print('move ok')

        regular_xml(newxmlPath,img,newimg)

    print('Totally rename {} files'.format(idx+1))
