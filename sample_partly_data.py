# encoding=utf-8
import os
import shutil
import random
# personal lib
from basicFun import FILES

if __name__ == "__main__":

    taskDir = '/home/cidi/Workspace/datasets/weather_database/cidi8typesWeatherData/数据源'
    outRoot = '/home/cidi/Workspace/datasets/weather_database/cidi8typesWeatherData/数据源_sampled'
    sample_num = 120

    FILES.mkdir(outRoot)

    dirs = os.listdir(taskDir)

    print(dirs)
    for dir_ in dirs:
        print(dir_)
        FILES.mkdir(os.path.join(outRoot, dir_))
        src_dir = os.path.join(taskDir, dir_)
        des_dir = os.path.join(outRoot, dir_)
        allImgs = FILES.get_sorted_files(src_dir)

        num_img = len(allImgs)

        if num_img > sample_num:
            random.seed(6)
            todo_imgs = random.sample(allImgs, sample_num)
        else:
            todo_imgs = allImgs

        # jpg move
        for img in todo_imgs:
            srcPath = os.path.join(src_dir, img)
            desPath = os.path.join(des_dir, img)
            shutil.copy(srcPath, desPath)
