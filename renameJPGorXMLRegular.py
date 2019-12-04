import os
from basicFun import FILES
dir1=r"/disk2/hao.yang/project/Qin/data/preProcess/tolabelImg/0501/switch_FengShi_simulate_img/"
dir2=dir1
preTitle='unload_FengShi_switch_simulate_'
endTitle=''
i=0
filelist=FILES.get_sorted_files(dir1)
for file in filelist:
	if ".jpg" in file:
	    # newfile='%06d'%i
	    newfile=file
	    os.rename(os.path.join(dir1,file),os.path.join(dir1,preTitle+newfile+endTitle+".jpg"))
	    try:
	    	os.rename(dir2+"/"+file.split('.')[0]+'.xml',dir2+"/"+preTitle+newfile+".xml")
	    except:
	    	print(file,"no xml")
	    i+=1
