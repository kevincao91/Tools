import xml.etree.ElementTree as ET
import os
import json
from basicFun import FILES,COCO
_DATA_DIR=r'.'
coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []
category_set = dict()
image_set = set()
category_item_id = 0
image_id = 20180000000
annotation_id = 0
# safe
# labelmap={1:'blue',2:'yellow',3:'other',4:'security',5:'safe_close',6:'safe_hide',7:'safe_open',8:'door_close',9:'door_open'}
#checkout
labelmap=COCO.labelmap_checkout
#unload
# labelmap = {1:'blue',2:'yellow',3:'other',4:'red',5:'tank_open',6:'tank_close',
# 7:'pipe_on',8:'clamp_on',9:'jug',10:'outfire',11:'truck'}
# gate
# labelmap={1:'blue',2:'yellow',3:'other'}
# phonescan
# labelmap={1:'phone',2:'scanner'}
# pos
# labelmap={1:'pos_use',2:'pos_free'}
# isle & guide
# labelmap = {1:'blue',2:'yellow',3:'other',4:'car',5:'truck',6:'bus',7:'motorcycle'}
# bill & card
# labelmap={1:'bill',2:'card'}
def setCatItem(lmap):
    for i in range(1,len(lmap)+1):
        category_item = dict()
        category_item['supercategory'] = 'none'
        category_item['id'] = i
        category_item['name'] = lmap[i]
        coco['categories'].append(category_item)
        category_set[lmap[i]] = i
# def addCatItem(name):
#     global category_item_id
#     category_item = dict()
#     category_item['supercategory'] = 'none'
#     category_item_id = mapLabel[name]
#     category_item['id'] = category_item_id
#     category_item['name'] = name
#     coco['categories'].append(category_item)
#     category_set[name] = category_item_id
#     return category_item_id

def addImgItem(file_name, size):
    global image_id
    if file_name is None:
        raise Exception('Could not find filename tag in xml file.')
    if size['width'] is None:
        raise Exception('Could not find width tag in xml file.')
    if size['height'] is None:
        raise Exception('Could not find height tag in xml file.')
    image_id += 1
    image_item = dict()
    image_item['id'] = image_id
    image_item['file_name'] = file_name + '.jpg'
    image_item['width'] = size['width']
    image_item['height'] = size['height']
    coco['images'].append(image_item)
    image_set.add(file_name)
    return image_id

def addAnnoItem(object_name, image_id, category_id, bbox):
    global annotation_id
    annotation_item = dict()
    annotation_item['segmentation'] = []
    seg = []
    #bbox[] is x,y,w,h
    #left_top
    seg.append(bbox[0])
    seg.append(bbox[1])
    #left_bottom
    seg.append(bbox[0])
    seg.append(bbox[1] + bbox[3])
    #right_bottom
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1] + bbox[3])
    #right_top
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1])

    annotation_item['segmentation'].append(seg)

    annotation_item['area'] = bbox[2] * bbox[3]
    annotation_item['iscrowd'] = 0
    annotation_item['ignore'] = 0
    annotation_item['image_id'] = image_id
    annotation_item['bbox'] = bbox
    annotation_item['category_id'] = category_id
    annotation_id += 1
    annotation_item['id'] = annotation_id
    coco['annotations'].append(annotation_item)

def parseXmlFiles(xml_path): 
    for f in os.listdir(xml_path):
        if not f.endswith('.xml'):
            continue
        bndbox = dict()
        size = dict()
        current_image_id = None
        current_category_id = None
        file_name = None
        size['width'] = None
        size['height'] = None
        size['depth'] = None
        xml_file = os.path.join(xml_path, f)
        # print(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))
        #elem is <folder>, <filename>, <size>, <object>
        for elem in root:
            current_parent = elem.tag
            current_sub = None
            object_name = None
            
            if elem.tag == 'folder':
                continue
            
            if elem.tag == 'filename':
                file_name = elem.text
                if file_name in category_set:
                    raise Exception('file_name duplicated')
                
            #add img item only after parse <size> tag
            elif current_image_id is None and file_name is not None and size['width'] is not None:
                if file_name not in image_set:
                    current_image_id = addImgItem(file_name, size)
                    # print('add image with {} and {}'.format(file_name, size))
                else:
                    raise Exception('duplicated image: {}'.format(file_name)) 
            #subelem is <width>, <height>, <depth>, <name>, <bndbox>
            for subelem in elem:
                bndbox ['xmin'] = None
                bndbox ['xmax'] = None
                bndbox ['ymin'] = None
                bndbox ['ymax'] = None
                
                current_sub = subelem.tag

                #option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
                for option in subelem:
                    if current_sub == 'bndbox':
                        if bndbox[option.tag] is not None:
                            raise Exception('xml structure corrupted at bndbox tag.')
                        bndbox[option.tag] = int(option.text)

                #only after parse the <object> tag
                if bndbox['xmin'] is not None:
                    bbox = []
                    #x
                    bbox.append(bndbox['xmin'])
                    #y
                    bbox.append(bndbox['ymin'])
                    #w
                    bbox.append(bndbox['xmax'] - bndbox['xmin'])
                    #h
                    bbox.append(bndbox['ymax'] - bndbox['ymin'])
                if current_parent == 'size':
                    if size[subelem.tag] is not None:
                        raise Exception('xml structure broken at size tag.')
                    size[subelem.tag] = int(subelem.text)
                elif current_parent == 'object' and subelem.tag == 'name':
                    object_name = subelem.text
                    if object_name not in category_set:
                        # current_category_id = addCatItem(object_name)
                        print("Unset catId {}\n".format(object_name))
                        exit()
                    else:
                        current_category_id = category_set[object_name]
                    if bbox == []:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_image_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_category_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    addAnnoItem(object_name, current_image_id, current_category_id, bbox )
                    
if __name__ == '__main__':
    xml_path = '/disk2/hao.yang/project/Qin/data/xmls/checkout/complete/xml_checkout_8651_test/'
    jsonDir='/disk2/hao.yang/project/Qin/data/jsons/checkout/'
    FILES.mkdir(jsonDir)
    if jsonDir:
        if xml_path[-1]=='/':
            xmlName=xml_path.split('/')[-2]
        else:
            xmlName=xml_path.split('/')[-1]
        json_file=os.path.join(jsonDir,xmlName+'.json')
    else:
        if xml_path[-1]=='/':
            json_file = xml_path[:-1]+'.json'
        else:
            json_file = xml_path+'.json'
    setCatItem(labelmap)
    parseXmlFiles(xml_path)
    json.dump(coco, open(json_file, 'w'))
