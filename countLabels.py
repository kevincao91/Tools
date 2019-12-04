#encoding=utf8
#所有xml文件内含box的数目
import os,sys
from bs4 import BeautifulSoup
import shutil
from basicFun import FILES
from basicFun import TXT
from tqdm import tqdm
if __name__=="__main__":
    labelDict={}
    xmlpath=sys.argv[1]
    index=0
    safeboxCount=0
    allxml=[x for x in FILES.get_sorted_files(xmlpath) if ".xml" in x]
    for xmlName in tqdm(allxml):
        xmlpath3=os.path.join(xmlpath,xmlName)
        txts=TXT.read_txt(xmlpath3)
        soup=BeautifulSoup(txts,"xml") #解析xml文
        section=soup.find_all('object') #通过object标签匹配所有相关的标签中的内容
        for sec in section:
            name=sec.find('name').get_text() # find函数只找到第一个相关的内容
            if name not in labelDict.keys():
                labelDict[name]=1
            else:
                labelDict[name]+=1
    print(xmlpath,'\nFILES=',len(allxml),"classes=",len(labelDict))
    print(labelDict.items())
