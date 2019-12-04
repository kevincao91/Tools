'Make a even validation set from a whole dataset'
import os,shutil,sys
from basicFun import XML,FILES
def filter_by_cate(allXmls,cateName):
	filteredXmls=[]
	viewCount=0
	xmlSum=len(allXmls)
	for xml in allXmls:
		xmlPath=os.path.join(xmlDir,xml)
		objs=XML.read_objects(xmlPath)
		for obj in objs:
			objName=obj['name']
			if objName == cateName:
				filteredXmls.append(xml)
		viewCount+=1
		sys.stdout.write('\rFiltering xmls >>{count:.2f}%'.format(count=100*float(viewCount)/xmlSum))
    	# sys.stdout.write('\r>> Detecting {name} {count:.2f}%'.format(name=videoPath.split('/')[-1],count=(100*float(i)/total_frames)))
		sys.stdout.flush()
	return filteredXmls
xmlDir=r"/DATACENTER2/hao.yang/project/Qin/checkout/FengShi/xml1383_8kinds/"
if xmlDir[-1]=='/':
    xmlTar = xmlDir[:-1]+'_val'
else:
    xmlTar = xmlDir+'_val'
FILES.mkdir(xmlTar)
# Get leastNum boxes of the cate at least 
leastNum=40
count=0
valCount=0
allXmls=FILES.get_sorted_files(xmlDir)
# Filter xmls having a box of a cate
cateName='pos_idle'
print('Start to filter xmls containing cate {}'.format(cateName))
filteredXmls=filter_by_cate(allXmls,cateName)
print('\nTotally {} xmls containing cate {}'.format(len(filteredXmls),cateName))
valRate=int(len(filteredXmls)/leastNum)
for xml in filteredXmls:
	if count%valRate==0:
		xmlPath=os.path.join(xmlDir,xml)
		tarPath=os.path.join(xmlTar,xml)
		shutil.copy(xmlPath,tarPath)
		valCount+=1
	count+=1
print('Made validation set with {} xmls'.format(valCount))