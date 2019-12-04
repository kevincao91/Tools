import os
import shutil
from basicFun import FILES
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
def sample_files(sampleDir,tarDir,remainNum):
    allFiles=FILES.get_sorted_files(sampleDir)
    filesCount=len(allFiles)
    print(filesCount)
    REMRATE=int(filesCount/remainNum)
    remRate=REMRATE
    count=int(REMRATE)+1
    fileNum=0
    for file in allFiles:
        if count-remRate>0:
            filePath=os.path.join(sampleDir,file)
            tarPath=os.path.join(tarDir,file)
            shutil.copy(filePath,tarPath)
            fileNum+=1
            remRate+=REMRATE
        count+=1    
srcDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/unload/xml_unload_38212_rdclamp_rmtube/'
tarDir='/DATACENTER4/hao.yang/project/Qin/data/xmls/unload/xml_unload_val/'
FILES.mkdir(tarDir)
sample_files(srcDir,tarDir,1000)
# xmlDir=r"E:\factory\voc\add_data\summary\rawImg\Tank_jl"
# jpgDir=r"E:\research\lackLabel\voc\img4206"
# xmlTar=r"E:\factory\voc\add_data\summary\rawImg\Tank_jl_lite"
# jpgTar=r"E:\research\lackLabel\voc\img2103_1"
# remainNum=70
# FILES.rm_mkdir(xmlTar)
# # FILES.rm_mkdir(jpgTar)
# allFiles=FILES.get_sorted_files(xmlDir)
# filesCount=len(allFiles)
# REMRATE=filesCount/remainNum
# remRate=REMRATE
# count=int(REMRATE)+1
# fileNum=0
# for file in allFiles:
# 	if count-remRate>0:
# 		filePath=xmlDir+'/'+file
# 		tarPath=xmlTar+'/'+file
# 		shutil.copy(filePath,tarPath)
# 		fileNum+=1
# 		remRate+=REMRATE
# 	count+=1
# copy_files_refer_dir(jpgDir,'.jpg',xmlTar,jpgTar)