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
    xmlDir=r'/media/kevin/DataSet/city1har/VOC2007/Annotations'
    setDir=r'/media/kevin/DataSet/city1har/VOC2007/ImageSets/Main'
    
    print(setDir)
    allSets=[x for x in FILES.get_sorted_files(setDir) if ".txt" in x]
    print(allSets)
    for setfile in allSets:
        setPath=os.path.join(setDir,setfile)
        print(setPath)
        keepLines=[]
        with open(setPath,'r') as f:
            lines = f.readlines()
            print(len(lines))
            
        for line in tqdm(lines):
            res = XML.read_objects(os.path.join(xmlDir,line[:-1]+'.xml'))
            if res :
                keepLines.append(line)
        print(len(keepLines))
        
        with open(setPath,'w') as f:
            f.writelines(keepLines)
                
    print('Totally regular {} xmls'.format(count))
