import os 
import random
from shutil import copyfile

def random_pick(img_src_path,img_dst_path,xml_src_path,xml_dst_path,num):
	img_src_file_list = os.listdir(img_src_path)
	img_dst_file_list = os.listdir(img_dst_path)
	xml_src_file_list = os.listdir(xml_src_path)
	# xml_dst_file_list = os.listdir(xml_dst_path)
	
	for i in range(num):
		tmp1 = random.randint(0,59000)

		if (img_src_file_list[tmp1] not in img_dst_file_list) and (img_src_file_list[tmp1][:-4]+'.xml' in xml_src_file_list): 
			copyfile(img_src_path+img_src_file_list[tmp1],img_dst_path+img_src_file_list[tmp1])
			print("复制 %s 图片成功" % img_src_file_list[tmp1]	)		 				
			copyfile(xml_src_path+img_src_file_list[tmp1][:-4]+'.xml',xml_dst_path+img_src_file_list[tmp1][:-4]+'.xml')
			print("复制 %s 注释成功" % img_src_file_list[tmp1][:-4]+'.xml'	)			
		else:
			pass		
			
			

if __name__ == '__main__':
	img_src_path = './traffic_JPEGImages/'
	img_dst_path = './traffic_random_pick/'
	xml_src_path = './traffic_Annotations/Annotations/'
	xml_dst_path = './traffic_Annotations_random_pick/'
	num = 2000
	random_pick(img_src_path,img_dst_path,xml_src_path,xml_dst_path,num)