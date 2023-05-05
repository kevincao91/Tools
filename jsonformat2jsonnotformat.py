import glob
import os
import json
from tqdm import tqdm

root_dir = '/home/cidi/Documents/标注资料/20230103-H5点云标注/zszn-20230309-output/output'


files_list = glob.glob(os.path.join(root_dir, '**','*.json'), recursive=True)

print(len(files_list))

for it in tqdm(files_list):
    # with open(it, 'r') as f:
    #     lines = f.readline()
    try:
        with open(it, 'r') as f:
            data = json.load(f)
        with open(it, 'w') as f:
            json.dump(data, f)
    except:
        print(it)
