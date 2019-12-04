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
def sample_random(sampleDir,tarDir,remainNum):
    allFiles=FILES.get_sorted_files(sampleDir)
    random.shuffle(allFiles)
    count=0
    for file in allFiles:
        if count<remainNum:
            filePath=os.path.join(sampleDir,file)
            tarPath=os.path.join(tarDir,file)
            shutil.move(filePath,tarPath)
        count+=1    
srcDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/safe/safe_FMXX_23743_total/'
tarDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/safe/safe_FMXX_23743_test/'
FILES.mkdir(tarDir)
sample_random(srcDir,tarDir,5000)