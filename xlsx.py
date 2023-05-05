import xlrd
import os
import time

import datetime
from xlrd import xldate_as_tuple

from moviepy.editor import *

# 从xlsx中读取时间段然后截取视频段落

# 时间字符串转换为秒
def timeTransform(time_str):
	#print(time_str)
	hour,minute,second = time_str.split(':')
	t = datetime.datetime(2019,1,1,int(hour), int(minute), int(second))
	return int((t-datetime.datetime(2019,1,1)).total_seconds())

def clip_video(video_path, str_starttime, str_endtime, output_path, idx):
	start_sec = timeTransform(str_starttime)
	end_sec = timeTransform(str_endtime)
	if start_sec > end_sec:
		print('出错:开始时间大于结束时间')
		return
	file_name = os.path.basename(video_path)
	name, ext = file_name.split('.')
	print("开始剪辑：{}-{}，共{}秒".format(str_starttime,str_endtime,end_sec-start_sec))
	clip = VideoFileClip(video_path).subclip(start_sec, end_sec)
	new_file = name + '_' +str(idx) +'_clip.' + ext
	clip.write_videofile(os.path.join(output_path,new_file))



video_file_root_path ='/DATACENTER2/ke.cao/oil_video_Data/all/' #视频路径
output_path = '/DATACENTER2/ke.cao/tool/clip_over/' #输出文件夹
file_path = '/DATACENTER2/ke.cao/tool/1-19.xlsx'



data = xlrd.open_workbook(file_path)
table = data.sheet_by_name('Sheet1')
nrows = table.nrows
ncols = table.ncols
print(nrows, ncols)


for row in range(1,nrows):
    print(row,'/',nrows)
    video_name =  table.cell(row,0).value
    video_path = os.path.join(video_file_root_path,video_name)
    print(video_path)
    for col in range(1,ncols,2):
        value1 = table.cell(row,col).value
        value2 = table.cell(row,col+1).value
        # print(row, col, value1)
        # print(row, col+1, value2)
        if value1 == '':
            break
        if table.cell(row,col).ctype == 3:
            date = xldate_as_tuple(table.cell(row,col).value,0)
            # print(date)
            str_starttime = str(date[3]) +":"+ str(date[4]) +":"+ str(date[5]) 
            # print(str_starttime)
        if table.cell(row,col+1).ctype == 3:
            date = xldate_as_tuple(table.cell(row,col+1).value,0)
            # print(date)
            str_endtime = str(date[3]) +":"+ str(date[4]) +":"+ str(date[5]) 
            # print(str_endtime)
        print(str_starttime,' --> ',str_endtime)
        
        
        clip_video(video_path, str_starttime, str_endtime, output_path, col)
 
 


