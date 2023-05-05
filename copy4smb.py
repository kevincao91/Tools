import os
import glob
from tqdm import tqdm
import shutil

src_root_dir = '/run/user/1000/gvfs/smb-share:server=172.16.201.241,share=cidiikuai/柳州柳汽项目/柳汽H5-001/'
dst_root_dir = '/run/user/1000/gvfs/sftp:host=172.16.201.101/home/cidi/72T/20230314-bag-selected'

dir_list = ['2022-11-11', '2022-11-14', '2022-11-15','2022-11-16','2022-11-18','2022-11-19',
            '2022-11-22', '2022-11-23', '2022-11-24','2022-11-28','2022-11-29','2022-11-30',
            '2022-12-02']

bag_list = []
for dir_ in dir_list:
    dir_path = os.path.join(src_root_dir, dir_, 'bag', '*.bag')

    tmp_list = glob.glob(dir_path)
    bag_list += tmp_list

    print(tmp_list)

for it in tqdm(bag_list):
    src = it
    name = os.path.split(src)[-1]
    dst = os.path.join(dst_root_dir, name)
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        print('save file to {}.'.format(dst))

