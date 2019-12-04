# encoding=utf8
import os
from basicFun import FILES
if __name__ == "__main__":
    count=0
    rmvDir=r"/DATACENTER3/yh/detectron/caffe2/detect/factory/people_longVideoAll/"
    referDirRoot=r"/DATACENTER3/yh/detectron/caffe2/detect/factory"
    # referDirNames=["tankClose","tankNoPipe","tankPipe","terribleCover"]
    referDirNames=["outXml"]
    referType=".xml"
    rmvType=".jpg"
    # referDirNames=["1","2","3"]
    allRmvs = [x for x in FILES.get_sorted_files(rmvDir) ]
    for referDirName in referDirNames:
        referDir=referDirRoot+'/'+referDirName
        allRefers=[x for x in FILES.get_sorted_files(referDir) if referType in x]
      # 审核为.jpg形成列表
        for rmv in allRmvs:
            if (rmv.split('.')[0]+referType) not in allRefers:
                removePath=rmvDir+'/'+rmv.split('.')[0]+rmvType
                # removePath=rmvDir+'/'+rmv
                os.remove(removePath)
                count+=1
    print("cancel {} files={}\n".format(rmvType,count))
