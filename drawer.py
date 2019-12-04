# coding=utf-8
import json
import glob
import cv2
import os

def draw_a_object(img,bbox,label):
	blue = (230, 213, 173)
	xmin=bbox[0]
	ymin=bbox[1]
	xmax=bbox[2]
	ymax=bbox[3]	
	cv2.rectangle(img, (xmin, ymin), (xmax, ymax), blue, 2)
	if label != " ":
		temp_frame = img.copy()
		temp_frame2 = img.copy()
		cv2.rectangle(temp_frame, (xmin-1,ymin-15), (xmax+1,ymin), (0,0,0),-1)
		img = cv2.addWeighted(temp_frame, 0.6, temp_frame2, 0.4 , 0, img)
		cv2.putText(img, str(label), (xmin+1, ymin - 6), cv2.FONT_HERSHEY_TRIPLEX, 0.3 , (255, 255, 255),1,cv2.LINE_AA)	
	return img

def draw_a_pic(frame_path,xml_path,out_put_path):
	frame=cv2.imread(frame_path)
	xml=open(xml_path)
	for n in xml:
		if '<object>' in n:
			try:
				label=next(xml).split('>')[1].split('<')[0]
			except StopIteration: 
				pass
		if '<bndbox>' in n:
			try:
				xmin=next(xml).split('>')[1].split('<')[0]
				ymin=next(xml).split('>')[1].split('<')[0]
				xmax=next(xml).split('>')[1].split('<')[0]
				ymax=next(xml).split('>')[1].split('<')[0]
			except StopIteration:
				pass
			xmin=int(float(xmin))
			ymin=int(float(ymin))
			xmax=int(float(xmax))
			ymax=int(float(ymax))
			bbox=[xmin,ymin,xmax,ymax]
			frame=draw_a_object(frame,bbox,label)

	img_name=os.path.join(out_put_path,os.path.basename(frame_path))
	print("write img to: ",img_name)
	cv2.imwrite(img_name, frame)

def draw_a_video(frame_path,xml_path,out_put_path,fps,video_name,video_size):
	video = cv2.VideoWriter(os.path.join(out_put_path,video_name), cv2.VideoWriter_fourcc(*'mp4v'), fps, video_size)
	print("init video file success.")
	print("out put path: ",os.path.join(out_put_path,video_name))
	xml=os.listdir(xml_path)
	xml.sort()
	xml_len=int(len(xml))
	for i in range(xml_len):
		open_xml=open(os.path.join(xml_path,xml[i]))
		img_path=os.path.join(frame_path,os.path.basename(xml[i].rstrip(".xml"))+".jpg")
		frame=cv2.imread(img_path)
		for n in open_xml:
			if '<object>' in n:
				try:
					label=next(open_xml).split('>')[1].split('<')[0]
				except StopIteration: 
					pass
			if '<bndbox>' in n:
				try:
					xmin=next(open_xml).split('>')[1].split('<')[0]
					ymin=next(open_xml).split('>')[1].split('<')[0]
					xmax=next(open_xml).split('>')[1].split('<')[0]
					ymax=next(open_xml).split('>')[1].split('<')[0]
				except StopIteration:
					pass
				xmin=int(float(xmin))
				ymin=int(float(ymin))
				xmax=int(float(xmax))
				ymax=int(float(ymax))
				bbox=[xmin,ymin,xmax,ymax]
				frame=draw_a_object(frame,bbox,label)
		frame=cv2.resize(frame,video_size)
		video.write(frame)
	video.release()
	cv2.destroyAllWindows()
	print("draw video file success.")
		
if __name__ == "__main__":

#------------------------------
	is_draw_video= True
	pic_path='/DATACENTER2/ke.cao/tool/unload_images'
	xml_path='/DATACENTER2/ke.cao/tool/unload_images_xml'
	out_put_path='/DATACENTER8/ke.cao/'
	fps = 24
	video_name='out.mp4'
	video_size = (1280, 720)
#------------------------------
	if is_draw_video:
		draw_a_video(pic_path,xml_path,out_put_path,fps,video_name,video_size)
	else:
		draw_a_pic(frame_path,xml_path,out_put_path)
