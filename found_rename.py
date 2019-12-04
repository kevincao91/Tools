import os,shutil
from basicFun import FILES
dir1=r"/disk2/hao.yang/project/Qin/data/preProcess/tolabelImg/0501/safe_cashbox_FengShi_simulate/"
des1=r"/disk2/hao.yang/project/Qin/data/preProcess/tolabelImg/0501/safe_cashbox_FengShi_simulate_img/"
dir2='/disk2/hao.yang/project/Qin/data/preProcess/tolabelImg/0501/xml/'
des2='/disk2/hao.yang/project/Qin/data/preProcess/tolabelImg/0501/labeled_tube_px/'
FILES.mkdir(des1)
FILES.mkdir(des2)
preTitle='safe_cashbox_FengShi_simulate_'
endTitle=''
i=0
filelist=FILES.get_sorted_files(dir1)
for file in filelist:
    if ".jpg" in file:
        newfileName='%06d'%i
        # newfileName=file
        # shutil.copy(os.path.join(dir1,file),os.path.join(des1,preTitle+newfileName+endTitle+".jpg"))
        shutil.copy(os.path.join(dir1,file),os.path.join(des1,preTitle+file))
        if os.path.exists(os.path.join(dir2,'unload_FengShi_tube_simulate_'+newfileName+endTitle+".xml")):
            shutil.copy(os.path.join(dir2,'unload_FengShi_tube_simulate_'+newfileName+endTitle+".xml"),os.path.join(des2,preTitle+file.replace('.jpg',".xml")))
        else:
            print(file,"no xml")
        i+=1
