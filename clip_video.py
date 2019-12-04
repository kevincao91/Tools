from moviepy.editor import *
import argparse
import datetime
import os




parser = argparse.ArgumentParser(description='Clip video')
parser.add_argument('--starttime',type=str,default='00:00:00')
parser.add_argument('--endtime',type=str,default='00:00:00')
parser.add_argument('--path',type=str,default='')#视频路径
parser.add_argument('--output',type=str,default='./')#输出文件夹
opt=parser.parse_args()


# 时间字符串转换为秒
def timeTransform(time_str):
	#print(time_str)
	hour,minute,second = time_str.split(':')
	t = datetime.datetime(2019,1,1,int(hour), int(minute), int(second))
	return int((t-datetime.datetime(2019,1,1)).total_seconds())


def main():
	start_sec = timeTransform(opt.starttime)
	end_sec = timeTransform(opt.endtime)
	if start_sec > end_sec:
		print('出错:开始时间大于结束时间')
		return
	file_name = os.path.basename(opt.path)
	name, ext = file_name.split('.')
	print("开始剪辑：{}-{}，共{}秒".format(opt.starttime,opt.endtime,end_sec-start_sec))
	clip = VideoFileClip(opt.path).subclip(start_sec, end_sec)
	new_file = name + '_clip.' + ext
	clip.write_videofile(os.path.join(opt.output,new_file))

main()
