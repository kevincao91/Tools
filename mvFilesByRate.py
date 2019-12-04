import os
import shutil
from basicFun import FILES
import random
def copy_files_refer_dir(FileDir,FileForm,ReferDir,xmlTar):
    allRefers=FILES.get_sorted_files(ReferDir)
    for refer in allRefers:
        file=refer.split('.')[0]+FileForm
        sourPath=os.path.join(FileDir,file)
        tarPath=os.path.join(xmlTar,file)
        try:
            shutil.copy(sourPath,tarPath)
        except:
            pass
sites=['FengShi','MingDeMen','XiWan']
for site in sites:
	for isle in range(1,6):
		outXmlDir="/disk2/hao.yang/project/Qin/data/imgs/isle/{}/isle{}_{}_img/".format(site,isle,site)
		volume=1000
		partition=1
		allFiles=FILES.get_sorted_files(outXmlDir)
		random.shuffle(allFiles)
		count=0
		for file in allFiles:
			if count<volume+volume*(partition-1)*0.2:
				count+=1
			else:
				# exit()
				# break
				partition+=1
				count=0
			# tar_outXmlDir='{}_partition{}'.format(outXmlDir,partition)
			pDir='/disk2/hao.yang/project/Qin/data/labelTask/isles/p{}'.format(partition)
			FILES.mkdir(pDir)
			tar_outXmlDir='/disk2/hao.yang/project/Qin/data/labelTask/isles/p{}/{}_isle{}'.format(partition,site,isle)
			FILES.mkdir(tar_outXmlDir)
			filePath=os.path.join(outXmlDir,file)
			tarPath=os.path.join(tar_outXmlDir,file)
			shutil.copy(filePath,tarPath)
# copy_files_refer_dir(jpgDir,'.jpg',outXmlDir,jpgTar)