#encoding=utf-8
'Filter xml files by some requirements'
import os
from bs4 import BeautifulSoup
from basicFun import XML
from basicFun import FILES
from basicFun import TXT
import shutil
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
def checkName(path,name):
    boxes=XML.read_object(path)
    for box in boxes:
        if box[0]==name :
            return 1
    return 0
def countObj(path):
    boxes=XML.read_object(path)
    return (len(boxes))
def changeXmlLabelName(path,labelDict):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    root=XML.del_tag(root,["13"])
    root=XML.chag_name(root,labelDict)
    XML.write_xml(tree,path)  
def find_all_cates(xmlDir):
    labelDict={}
    allXmls=FILES.get_sorted_files(xmlDir)
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml")
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text() # find函数只找到第一个相关的内容
            if name not in labelDict.keys():
                labelDict[name]=1
            else:
                labelDict[name]+=1
    return labelDict.keys()
def find_most_cates_with_cate(xmlDir,cate,savedCates):
    maxCates=0
    allXmls=FILES.get_sorted_files(xmlDir)
    for xml in allXmls:
        labelDict={}
        xmlPath=os.path.join(xmlDir,xml)
        tarPath=os.path.join(tarDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text() # find函数只找到第一个相关的内容
            if name not in labelDict.keys():
                labelDict[name]=1
            else:
                labelDict[name]+=1
        if cate in labelDict.keys():
            if len(labelDict)>maxCates:
                maxCates=len(labelDict)
                maxXml=xmlPath
                maxTar=tarPath
                maxAddCates=labelDict.keys()
    print("maxXml={}, maxTar={}".format(maxXml,maxTar))
    shutil.copy(maxXml,maxTar)
    for maxAddCate in maxAddCates:
        savedCates.append(maxAddCate)
def filter_short_cates(xmlDir,cates):
    allXmls=FILES.get_sorted_files(xmlDir)
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        tarPath=os.path.join(tarDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text()
            if name in cates:
                bndb=obj.find("bndbox")
                xsize=int(bndb.find('xmax').text)-int(bndb.find('xmin').text)
                ysize=int(bndb.find('ymax').text)-int(bndb.find('ymin').text)
                if xsize>ysize*0.9:
                    shutil.copy(xmlPath,tarPath)
                    break
def filter_xmls_with_cates(xmlDir,cates):
    allXmls=FILES.get_sorted_files(xmlDir)
    ii=0
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        tarPath=os.path.join(tarDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text()
            if name in cates:
                shutil.copy(xmlPath,tarPath)
                ii+=1
                break
def move_xmls_with_cates(xmlDir,cates):
    allXmls=FILES.get_sorted_files(xmlDir)
    ii=0
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        tarPath=os.path.join(tarDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text()
            if name in cates:
                shutil.move(xmlPath,tarPath)
                ii+=1
                break
def filter_xmls_without_cates(xmlDir,cates):
    allXmls=FILES.get_sorted_files(xmlDir)
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        tarPath=os.path.join(tarDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        noTruck=1
        for obj in objs:
            name=obj.find('name').get_text()
            if name in cates:
                noTruck=0
                break
        if noTruck==1:    
            shutil.copy(xmlPath,tarPath)
def find_xmls_with_all_cates(xmlDir):
    savedCates=[]
    allCates=find_all_cates(xmlDir)
    for cate in allCates:
        if cate not in savedCates:
            print("cate {} not in savedCates {}\n".format(cate,savedCates))
            find_most_cates_with_cate(xmlDir,cate,savedCates)
def filter_lack_helmet(xmlDir):
    personCates=['person']
    helmetCates=['red','yellow','blue','white','orange']
    allXmls=FILES.get_sorted_files(xmlDir)
    for xml in allXmls:
        numPer=0
        numHel=0
        xmlPath=os.path.join(xmlDir,xml)
        lackPath=os.path.join(tarDir,xml)
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text()
            if name in personCates:
                numPer+=1
            elif name in helmetCates:
                numHel+=1
            else:
                print("Lack of category {} set in function filter_lack_helmet".format(name))
        if numPer>numHel:
            shutil.copy(xmlPath,lackPath)
def find_xmls_with_minimal_size_of_this_cate(xmlDir,cate):
    allXmls=FILES.get_sorted_files(xmlDir)
    MinW=9999
    MinH=9999
    MinA=MinW*MinH
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        wMinPath=os.path.join(tarDir,'{}_wMin.xml'.format(cate))
        hMinPath=os.path.join(tarDir,'{}_hMin.xml'.format(cate))
        aMinPath=os.path.join(tarDir,'{}_aMin.xml'.format(cate))
        txts=TXT.read_txt(xmlPath)
        soup=BeautifulSoup(txts,"xml") 
        objs=soup.find_all('object')
        for obj in objs:
            name=obj.find('name').get_text()
            if name ==cate:
                xmin=int(obj.find('xmin').get_text())
                xmax=int(obj.find('xmax').get_text())
                ymin=int(obj.find('ymin').get_text())
                ymax=int(obj.find('ymax').get_text())
                width=xmax-xmin
                height=ymax-ymin
                area=width*height
                if width<MinW:
                    MinW=width
                    shutil.copy(xmlPath,wMinPath)
                if height<MinH:
                    MinH=height
                    shutil.copy(xmlPath,hMinPath)
                if area<MinA:
                    MinA=area
                    shutil.copy(xmlPath,aMinPath)
    print("cate: {} MinW={}, MinH={}, MinA={}".format(cate,MinW,MinH,MinA))                
def find_xmls_with_minimal_size_of_each_cate(xmlDir):
    allCates=find_all_cates(xmlDir)
    for cate in allCates:
        find_xmls_with_minimal_size_of_this_cate(xmlDir,cate)
if __name__=="__main__":
    xmlDir=r'/DATACENTER4/hao.yang/project/Qin/data/xmls/checkout/xml_checkout_10972_total/'   
    tarDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/checkout/pos_use/'
    FILES.rm_mkdir(tarDir)
    # Uncomment to find some xmls containing all categories and copy matching jpgs
    # find_xmls_with_all_cates(xmlDir)
    # Uncomment to find xmls and jpgs containing given cates
    cates=['pos_use']
    # filter_short_cates(xmlDir,cates)
    filter_xmls_with_cates(xmlDir,cates)
    # move_xmls_with_cates(xmlDir,cates)
    # filter_xmls_without_cates(xmlDir,cates)
    # Uncomment to find boxes with minimal area, minimal width and minimal height of each category
    # find_xmls_with_minimal_size_of_each_cate(xmlDir)
    # Uncomment to filter xml and jpg whose amount of label_person > label_helmet
    # filter_lack_helmet(xmlDir)
    # Uncomment to copy jpgs referring xmls
    jpgDir=r"/DATACENTER4/hao.yang/project/Qin/data/imgs/checkout/imgs_labeled_all_10972/"
    jpgTar=tarDir
    FILES.mkdir(jpgTar)
    FILES.shutil_by_refer(tarDir,'.xml','.jpg',jpgDir,jpgTar)
