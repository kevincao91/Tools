#encoding=utf-8
# 
import os,cv2,sys
import numpy as np
import glob
from PIL import Image  
from PIL import ImageStat #就靠他了
from tqdm import tqdm

class info_count():
    def init(self, txt=None):
        self.info={}
        self.num=0
        #print('init')
        
        if txt:
            with open(txt, 'r') as f:
                lines = f.readlines()
            for line in lines:
                k, v = int(line.split()[0]), int(line.split()[1])
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


label_map=['sunny', 'rainy', 'littlefog', 'moderatefog', 'densefog', 'snow']

def analyze_pic(path):
    
    class_ = os.path.split(path)[-2][-1]
    #print(class_)
    class_str = label_map[int(class_)]

    if class_str not in count.info:
        count.addtag(class_str)
    else:
        count.update(class_str)
    count.count()
    
    image=cv2.imread(path)
    height=image.shape[0]
    width=image.shape[1]
    scale = round(np.sqrt(width*height))
    
    nn=int(scale/25)+1
    scale = nn*25
    
    if scale not in count2.info:
        count2.addtag(scale)
    else:
        count2.update(scale)
    count2.count()
    if class_ == '0':
        im = Image.open(path).convert('L')
        stat = ImageStat.Stat(im)
        count3.info[count3.num]=stat.mean[0]
        count3.count()
    elif class_ == '1':
        im = Image.open(path).convert('L')
        stat = ImageStat.Stat(im)
        count4.info[count4.num]=stat.mean[0]
        count4.count()
    elif class_ == '2':
        im = Image.open(path).convert('L')
        stat = ImageStat.Stat(im)
        count5.info[count5.num]=stat.mean[0]
        count5.count()
    elif class_ == '3':
        im = Image.open(path).convert('L')
        stat = ImageStat.Stat(im)
        count6.info[count6.num]=stat.mean[0]
        count6.count()
    elif class_ == '4':
        im = Image.open(path).convert('L')
        stat = ImageStat.Stat(im)
        count7.info[count7.num]=stat.mean[0]
        count7.count()
    elif class_ == '5':
        im = Image.open(path).convert('L')
        stat = ImageStat.Stat(im)
        count8.info[count8.num]=stat.mean[0]
        count8.count()
    
if __name__=="__main__":
    
    global count, count2, count3, count4,count5, count6, count7, count8
    count = info_count()
    count.init()
    count2 = info_count()
    count2.init()
    count3 = info_count()
    count3.init()
    count4 = info_count()
    count4.init()
    count5 = info_count()
    count5.init()
    count6 = info_count()
    count6.init()
    count7 = info_count()
    count7.init()
    count8 = info_count()
    count8.init()
    
    imgDir=r'/media/kevin/备份/weather/fast-MPN-COV/82CK6typesWeatherTestData/ImageNet'
    outDir='/media/kevin/办公/中文期刊 天气分类/word picture'
    
    print(imgDir)
    
    for root, dirs, filenames in os.walk(imgDir):
        for dir_ in dirs:
            print('dir', dir_)
            for file_ in tqdm(glob.glob(os.path.join(root, dir_, '*.*'))):
                analyze_pic(file_)
                #count.print()
    print('Totally count {} pictures'.format(count.num))
    
    
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

    '''
    count.init('src.txt')
    count.print()
    '''
    
    labels = count.get_labels()
    values = count.get_values()

     
    df = pd.DataFrame({'weather': labels,
                       'number': values})#生成
    #print(df)
    
    plt.figure(figsize = (8, 3))
    ax = sns.barplot(x=df['weather'], y=df["number"], data=df)

    # 旋转轴刻度上文字方向
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.title('The Number of Different Weather Pictures')
    out_path = os.path.join(outDir, "The Number of Different Weather Pictures.png")
    plt.savefig(out_path,dpi=500,bbox_inches='tight')
    plt.show()

    
    labels = count2.get_labels()
    values = count2.get_values()
     
    df = pd.DataFrame({'scale': labels,
                       'number': values})#生成
    
    plt.figure(figsize = (8, 3))
    ax = sns.barplot(x=df['scale'], y=df["number"], data=df)
    plt.xlim(0,50)  # 注意 按照个数数数
    # 旋转轴刻度上文字方向
    ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)
    plt.title('Picture Scale Distribution')
    out_path = os.path.join(outDir, "Picture Scale Distribution.png")
    plt.savefig(out_path,dpi=500,bbox_inches='tight')
    plt.show()
    
    
    labels = count3.get_labels()
    values = count3.get_values()
    df1 = pd.DataFrame({'index': labels,
                       'brightness': values})#生成
    
    labels = count4.get_labels()
    values = count4.get_values()
    df2 = pd.DataFrame({'index': labels,
                       'brightness': values})#生成
    
    labels = count5.get_labels()
    values = count5.get_values()
    df3 = pd.DataFrame({'index': labels,
                       'brightness': values})#生成
    
    labels = count6.get_labels()
    values = count6.get_values()
    df4 = pd.DataFrame({'index': labels,
                       'brightness': values})#生成
    
    labels = count7.get_labels()
    values = count7.get_values()
    df5 = pd.DataFrame({'index': labels,
                       'brightness': values})#生成
                       
    labels = count8.get_labels()
    values = count8.get_values()
    df6 = pd.DataFrame({'index': labels,
                       'brightness': values})#生成        
    #=======分布图=======
    plt.figure(figsize = (8, 3))
    X1 = df1['brightness']
    X2 = df2['brightness']
    X3 = df3['brightness']
    X4 = df4['brightness']
    X5 = df5['brightness']
    X6 = df6['brightness']

    # print(X)
    ax = sns.distplot(X1, bins = 60, hist = False, kde = True, norm_hist = False,
                rug = False, vertical = False,
                label = label_map[0], axlabel = 'Brightness')
    ax = sns.distplot(X2, bins = 60, hist = False, kde = True, norm_hist = False,
                rug = False, vertical = False,
                label = label_map[1], axlabel = 'Brightness')
    ax = sns.distplot(X3, bins = 60, hist = False, kde = True, norm_hist = False,
                rug = False, vertical = False,
                label = label_map[2], axlabel = 'Brightness')
    ax = sns.distplot(X4, bins = 60, hist = False, kde = True, norm_hist = False,
                rug = False, vertical = False,
                label = label_map[3], axlabel = 'Brightness')
    ax = sns.distplot(X5, bins = 60, hist = False, kde = True, norm_hist = False,
                rug = False, vertical = False,
                label = label_map[4], axlabel = 'Brightness')
    ax = sns.distplot(X6, bins = 60, hist = False, kde = True, norm_hist = False,
                rug = False, vertical = False,
                label = label_map[5], axlabel = 'Brightness')
    #ax.set_xticks(np.linspace(0, 255, 37))
    #plt.xlim(-0.5,260)
    plt.legend(loc = 'upper right', ncol = 1) # ajust ncol to fit the space
    plt.title('Picture Brightness Distribution')
    out_path = os.path.join(outDir, "Picture Brightness Distribution.png")
    plt.savefig(out_path,dpi=500,bbox_inches='tight')
    plt.show()

    
