# encoding=utf8
import os
import shutil
from basicFun import FILES
from tqdm import tqdm
if __name__ == "__main__":
    count=0
    srcDir=r"/DATACENTER4/hao.yang/project/Qin/data/imgs/safe/safe_CFMXX_img_divided/"
    tarDir=r"/DATACENTER4/hao.yang/project/Qin/data/imgs/safe/safe_FMXX_img/"
    allJpgs=[x for x in FILES.list_all_filePaths(srcDir) if '.jpg' in x]
    FILES.mkdir(tarDir)
    for jpgPath in tqdm(allJpgs):
        shutil.copy(jpgPath,os.path.join(tarDir,jpgPath.split('/')[-1]))
        count+=1
    print("copy jpgs:",count)