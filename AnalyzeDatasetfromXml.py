#encoding=utf-8
# 
import os,cv2,sys
from basicFun import XML,FILES,COCO
from tqdm import tqdm
import numpy as np

class info_count():
    def init(self, txt=None):
        self.info={}
        self.num=0
        print('init')
        
        if txt:
            with open(txt, 'r') as f:
                lines = f.readlines()
            for line in lines:
                k, v = line.split()[0], int(line.split()[1])
                self.info[k]=v
            print('load data')

    def count(self):
            self.num=self.num+1

    def addtag(self, name):
            self.info[name]=1

    def update(self, name):
            num = self.info[name]
            num += 1
            self.info[name] = num

    def print(self):
        for key in self.info:
            print(key, self.info[key])
        print('--')

    def get_labels(self):
        labels=[]
        for key in self.info:
            labels.append(key)
        print(labels)
        return labels
        
    def get_values(self):
        values=[]
        for key in self.info:
            values.append(self.info[key])
        print(values)
        return values

def analyze_xml(path):

    objs = XML.read_objects(path)
    #print(objs)

    for obj in objs:
        name = obj['name']
        '''
        if name in ['、', 'microbus_foreign\n', 'micorbus_foreign', 'car_pickup', 'truck_foregin', 'suv_foreign']:
            print(path)
            print(obj)
            exit()
        '''
        if name not in count.info:
            count.addtag(name)
        else:
            count.update(name)
        count.count()
        
        xmin = int(obj['xmin'])
        ymin = int(obj['ymin'])
        xmax = int(obj['xmax'])
        ymax = int(obj['ymax'])
        w = xmax - xmin
        h = ymax - ymin
        scale = round(np.sqrt(w*h))
        
        nn=int(scale/25)+1
        scale = nn*25
        
        '''
        if scale >2000:
            print(path)
            print(obj)
            exit()
        '''
        
        if scale not in count2.info:
            count2.addtag(scale)
        else:
            count2.update(scale)
        count2.count()

    
if __name__=="__main__":
    global count, scale_list, count2
    scale_list = []
    count = info_count()
    count.init()
    count2 = info_count()
    count2.init()
    
    imgDir=r'/media/kevin/娱乐/xizang_database/testdata/1125/JPEGImages'
    xmlDir=r'/media/kevin/娱乐/xizang_database/testdata/1125/all_Annotations_no_change_label'
    
    print(xmlDir)
    allXmls=[x for x in FILES.get_sorted_files(xmlDir) if ".xml" in x]

    for xml in tqdm(allXmls):
        xmlPath=os.path.join(xmlDir,xml)
        imgPath=os.path.join(imgDir,xml.replace('.xml','.jpg'))

        analyze_xml(xmlPath)
    count.print()
    print('Totally count {} targets'.format(count.num))
    
    
    # -*- coding: utf-8 -*-
    import pandas as pd
    import numpy as np
    import sys
    #reload(sys)
    #sys.setdefaultencoding('utf8')
    # from pylab import *
    #mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']#指定默认字体
    #mpl.rcParams['axes.unicode_minus'] =False # 解决保存图像是负号'-'显示为方块的问题
    #from sqlalchemy import create_engine
    import seaborn as sns
    import matplotlib.pyplot as plt

    #count.init('src.txt')
    #count.print()

    labels = count.get_labels()
    values = count.get_values()

     
    df = pd.DataFrame({'labels': labels,
                       'values': values})#生成
    print(df)
    
    plt.figure(figsize = (18, 8))
    ax = sns.barplot(x=df['labels'], y=df["values"], data=df)

    # 旋转轴刻度上文字方向
    ax.set_xticklabels(ax.get_xticklabels(), rotation=-30)
    plt.show()
    
    
    
    labels = count2.get_labels()
    values = count2.get_values()
     
    df = pd.DataFrame({'labels': labels,
                       'values': values})#生成
    print(df)
    
    plt.figure(figsize = (18, 8))
    ax = sns.barplot(x=df['labels'], y=df["values"], data=df)
    plt.xlim(-5,50)
    # 旋转轴刻度上文字方向
    ax.set_xticklabels(ax.get_xticklabels(), rotation=-30)
    plt.show()
    
