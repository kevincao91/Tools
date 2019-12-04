#encoding=utf-8
#二级目录下的jpg文件复制到一个文件夹
import os
import shutil
import time
from basicFun import FILES
if __name__=="__main__":
    timeStart=time.clock()
    roots="/DATACENTER4/hao.yang/project/Qin/data/preProcess/extractFrame/"
    rootsName=['0706_checkout']
    for rootName in rootsName:
        rootdir=os.path.join(roots,rootName)
        tardir=os.path.join(roots,rootName+"All") #不用创建
        print(rootdir,tardir)
        i=1
        if os.path.exists(rootdir):
            FILES.mkdir(tardir)
            alldirs=FILES.get_sub_dirs(rootdir)
            for dirName in alldirs:
                if 'test' in dirName:
                    continue
                dirpath=os.path.join(rootdir,dirName)
                # print(dirpath)
                alljpg=sorted([x for x in FILES.get_files(dirpath) if ".jpg" in x])#审核为.jpg形成列表
                for jpg in alljpg:
                    # rename
                    # newJpg=dirpath.split("/")[-1]+str("%06d"%i)+".jpg"
                    newJpg='{}_{}'.format(dirName,jpg)
                    # newJpg=jpg
                    i+=1
                    oldpath=os.path.join(dirpath,jpg)
                    newpath=os.path.join(tardir,newJpg)
                    shutil.copy(oldpath,newpath)
        print(time.clock()-timeStart)


# i=1
# dir1=r"E:\BUS\BUS1"
# filelist=os.listdir(dir1) 
# for file in filelist:
#     #newfile="%06d"%int(file.split('.')[0])
#     newfile="%06d"%i
#     os.rename(dir1+"/"+file,dir1+"/"+str(newfile)+".jpg")
#     i+=1
