#encoding=utf8
#所有jpg文件内含box的数目
#统计二级目录下jpg的数目
from basicFun import FILES
import sys
if __name__=="__main__":
    rootDir=sys.argv[1]
    allJpgs=[x for x in FILES.list_all_files(rootDir) if '.jpg' in x]
    print (len(allJpgs))
