#encoding=utf-8
import os
import shutil
import time
from basicFun import FILES
jpgRoot=r"/DATACENTER2/yh/dataRoom/gasStation/tank/train/sj18JunFrames"
if __name__=="__main__":
    remainNum=500
    start = time.time()
    jpgDirs=FILES.get_sub_dirs(jpgRoot)
    for dirName in jpgDirs:
        jpgDir=jpgRoot+'/'+dirName
        allJpgs=FILES.get_sorted_files(jpgDir)
        jpgCount=len(allJpgs)
        if jpgCount>3000:
            for jpg in allJpgs[remainNum:]:
                jpgPath=os.path.join(jpgDir,jpg)
                os.remove(jpgPath)

# def removeRemain(rmdir,remainNum)：
#   allFiles=FILES.get_sorted_files(rmdir)
#   filesCount=len(rmdir)
#   for 
#   remRate=REMRATE
#   # print(rmRate)
#   count=int(REMRATE)+1
#   fileNum=0
#   for file in allFiles:
#       if count-remRate>0:
#           filePath=dirDir+'/'+file
#           tarPath=tarDir+'/'+file
#           shutil.copy(filePath,tarPath)
#           # print(count)
#           fileNum+=1
#           remRate+=REMRATE
#       count+=1
#   print(fileNum)