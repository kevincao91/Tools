#encoding=utf-8
# Element.remove()
# Element.findall() finds only elements with a tag which are direct children of the current element
import os
from basicFun import XML
from basicFun import FILES
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
def add_cates(xmlPath,referPath,addCates):
    addBoxes=XML.read_objects(referPath)
    tree = ET.ElementTree(file=xmlPath)
    root = tree.getroot()
    # root=XML.del_tag(root,['3','9','13'])
    # print(addBoxes)
    for box in addBoxes:
        if box['name'] in addCates:
            root=XML.add_tag(root,box)
    XML.write_xml(tree,xmlPath)     
def add_new_cates(xmlPath,referPath,addCates):
    addBoxes=XML.read_objects(referPath)
    tree = ET.ElementTree(file=xmlPath)
    root = tree.getroot()
    root=XML.del_tag(root,addCates)
    # print(addBoxes)
    for box in addBoxes:
        if box['name'] in addCates:
            root=XML.add_tag(root,box)
    XML.write_xml(tree,xmlPath)           
if __name__=="__main__":
    # imgDir=r"F:\gasStation\tank\regular_dataset\SanJiang_tankbox\checked\no_pipe"
    xmlDir=r'/DATACENTER4/hao.yang/project/Qin/data/xmls/isle/isle_23174_cover_xml/'
    referDir=r"/DATACENTER4/hao.yang/project/Qin/data/xmls/isle/isle_23174_cover_cover/"    
    addCates=['cover']
    # addCates=['car','motorcycle','truck','bus']
    # addCates=['blue','yellow','other','security','red','gray']
    # addCates=['tank_close','tank_open']
    # addCates=['cashbox_close','cashbox_open']
    # addCates=['safe_close','safe_hide','safe_open','door_close','door_open']
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]
    for xml in allXmls:
        xmlPath=os.path.join(xmlDir,xml)
        referPath=os.path.join(referDir,xml)
        if os.path.exists(referPath):
            add_new_cates(xmlPath,referPath,addCates)
