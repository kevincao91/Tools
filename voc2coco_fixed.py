import json
import cv2
import glob
import numpy as np
import PIL.Image
import os
import sys
import xml.etree.ElementTree as ET

def text(node_lis):
    return {node.tag: node.text for node in node_lis}

class PascalVOC2coco(object):

    def __init__(self, xml=[], save_json_path='./instances.json', categories=[]):
        '''
        :param xml: 所有Pascal VOC的xml文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.xml = xml
        self.save_json_path = save_json_path
        self.images = []
        self.categories = categories
        self.annotations = []
        self.label = []
        self.annID = 1
        self.height = 0
        self.width = 0
        if len(categories) == 0:
            self.auto_annotation_id = True
        else:
            self.auto_annotation_id = False
        self.save_json()

    def data_transfer(self):
        print('Write {}'.format(self.save_json_path))
        for num, json_file in enumerate(self.xml):

            sys.stdout.write('\r>> Converting image %d/%d' % (
                num + 1, len(self.xml)))
            sys.stdout.flush()

            self.json_file = json_file
            self.num = num
            path = os.path.dirname(self.json_file)
            path = os.path.dirname(path)

            tree = ET.parse(json_file)
            root = tree.getroot()

            filename = root.find('filename').text
            if not filename.endswith('.jpg'):
                filename += '.jpg'
            self.file_name = filename
            self.path = os.path.join(path, 'SegmentationObject', self.file_name.split('.')[0] + '.png')

            size = root.find('size')

            size_dict = text(size)
            self.width, self.height = int(size_dict['width']), int(size_dict['height'])
            self.images.append(self.image())

            for obj in root.findall('object'):
                self.supercategory = obj.find('name').text
                if self.auto_annotation_id:
                    if self.supercategory not in self.label:
                        self.categories.append(self.category())
                        self.label.append(self.supercategory)
                bndbox = text(obj.find('bndbox'))
                x1, y1, x2, y2 = int(bndbox['xmin']), int(bndbox['ymin']), int(bndbox['xmax']), int(bndbox['ymax'])
                self.rectangle = [x1, y1, x2, y2]
                self.bbox = [x1, y1, x2 - x1, y2 - y1]  # COCO 对应格式[x,y,w,h]
                self.annotations.append(self.annotation())
                self.annID += 1

        sys.stdout.write('\n')
        sys.stdout.flush()


    def image(self):
        image_dict = {}
        image_dict['height'] = self.height
        image_dict['width'] = self.width
        image_dict['id'] = self.num + 1
        image_dict['file_name'] = self.file_name
        return image_dict


    def category(self):
        category_dict = {}
        category_dict['supercategory'] = self.supercategory
        category_dict['id'] = len(self.label) + 1  # 0 默认为背景
        category_dict['name'] = self.supercategory
        return category_dict


    def annotation(self):
        annotation_dict = {}
        annotation_dict['segmentation'] = [list(map(float, self.getsegmentation()))]
        annotation_dict['iscrowd'] = 0
        annotation_dict['image_id'] = self.num + 1
        annotation_dict['bbox'] = self.bbox
        annotation_dict['category_id'] = self.getcatid(self.supercategory)
        annotation_dict['id'] = self.annID
        annotation_dict['area'] = self.bbox[-2] * self.bbox[-1]
        return annotation_dict


    def getcatid(self, label):
        for category in self.categories:
            if label == category['name']:
                return category['id']
        return 0


    def getsegmentation(self):
        try:
            mask_1 = cv2.imread(self.path, 0)
            mask = np.zeros_like(mask_1, np.uint8)
            rectangle = self.rectangle
            mask[rectangle[1]:rectangle[3], rectangle[0]:rectangle[2]] = mask_1[rectangle[1]:rectangle[3],
                                                                         rectangle[0]:rectangle[2]]

            # 计算矩形中点像素值
            mean_x = (rectangle[0] + rectangle[2]) // 2
            mean_y = (rectangle[1] + rectangle[3]) // 2

            end = min((mask.shape[1], int(rectangle[2]) + 1))
            start = max((0, int(rectangle[0]) - 1))

            flag = True
            for i in range(mean_x, end):
                x_ = i;
                y_ = mean_y
                pixels = mask_1[y_, x_]
                if pixels != 0 and pixels != 220:  # 0 对应背景 220对应边界线
                    mask = (mask == pixels).astype(np.uint8)
                    flag = False
                    break
            if flag:
                for i in range(mean_x, start, -1):
                    x_ = i;
                    y_ = mean_y
                    pixels = mask_1[y_, x_]
                    if pixels != 0 and pixels != 220:
                        mask = (mask == pixels).astype(np.uint8)
                        break
            self.mask = mask

            return self.mask2polygons()

        except:
            return [0]


    def mask2polygons(self):
        contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 找到轮廓线
        bbox = []
        for cont in contours[1]:
            [bbox.append(i) for i in list(cont.flatten())]
        return bbox


    def getbbox(self, points):
        polygons = points
        mask = self.polygons_to_mask([self.height, self.width], polygons)
        return self.mask2box(mask)


    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        # return [(left_top_r,left_top_c),(right_bottom_r,right_bottom_c)]
        # return [(left_top_c, left_top_r), (right_bottom_c, right_bottom_r)]
        # return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]  # [x1,y1,x2,y2]
        return [left_top_c, left_top_r, right_bottom_c - left_top_c,
                right_bottom_r - left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式


    def polygons_to_mask(self, img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask


    def data2coco(self):
        coco_dict = {}
        coco_dict['images'] = self.images
        coco_dict['type'] = 'instances'
        coco_dict['categories'] = self.categories
        coco_dict['annotations'] = self.annotations
        return coco_dict


    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4)


base_paths = ['/DATACENTER4/hao.yang/project/Qin/data/xmls/checkout/']


def search_for_annotation(result, path):
    for root, dirnames, filenames in os.walk(path):
        if 'total' in root:
            result += [root]
    return result


# python3
from functools import reduce

annotation_paths_candidates = reduce(search_for_annotation, base_paths, [])
print(annotation_paths_candidates)
categories = []
categories = [{'supercategory': 'smallobject', 'id': 1, 'name': 'phone'}, ]
categories= [{"supercategory": "none", "id": 1, "name": "blue"}, {"supercategory": "none", "id": 2, "name": "yellow"}, {"supercategory": "none", "id": 3, "name": "other"}, {"supercategory": "none", "id": 4, "name": "hand"}, {"supercategory": "none", "id": 5, "name": "phone"}, {"supercategory": "none", "id": 6, "name": "scanner"}, {"supercategory": "none", "id": 7, "name": "pos_free"}, {"supercategory": "none", "id": 8, "name": "pos_use"}, {"supercategory": "none", "id": 9, "name": "bill"}, {"supercategory": "none", "id": 10, "name": "card"}]
for path in annotation_paths_candidates:
    xml_file = glob.glob(path + '/*.xml')
    obj = PascalVOC2coco(xml_file, path + '/instances.json', categories=categories)
    print('class count = {}'.format(len(obj.categories)))
    print(obj.categories)
