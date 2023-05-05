# -*- coding: UTF-8 -*-
 
import os
import imageio
import PIL.Image as Image
import numpy as np
 
def create_gif(image_list, gif_name):
 
    frames = []
    for image_name in image_list:
        if image_name.endswith('.jpg') or image_name.endswith('.png'):
            print(image_name)
            img = imageio.imread(image_name)
            # img = Image.fromarray(img).resize((710,400),Image.ANTIALIAS)
            frames.append(img)
        else:
            print(image_name, ' no support!!')
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.5)
 
    return
 
def concatx2_create_gif(listA, listB, gif_name):
 
    frames = []
    for image_nameA, image_nameB in zip(listA, listB):
        if (image_nameA.endswith('.jpg') or image_nameA.endswith('.png')) and \
            (image_nameB.endswith('.jpg') or image_nameB.endswith('.png')):
            print(image_nameA, image_nameB)
            imgA = imageio.imread(image_nameA)
            imgA = Image.fromarray(imgA).resize((640,360),Image.ANTIALIAS)
            imgB = imageio.imread(image_nameB)
            imgB = Image.fromarray(imgB).resize((640,360),Image.ANTIALIAS)
            img = np.concatenate([imgA, imgB], axis=1)
            frames.append(img)
        else:
            print(image_nameA, image_nameB, ' no support!!')
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.5)
 
    return

def concatx4_create_gif(listA, listB, listC, listD, gif_name):
 
    frames = []
    for image_nameA, image_nameB, image_nameC, image_nameD in zip(listA, listB, listC, listD):
        if (image_nameA.endswith('.jpg') or image_nameA.endswith('.png')) and \
            (image_nameB.endswith('.jpg') or image_nameB.endswith('.png')):
            print(image_nameA, image_nameB)
            imgA = imageio.imread(image_nameA)
            imgA = Image.fromarray(imgA).resize((640,360),Image.ANTIALIAS)
            imgB = imageio.imread(image_nameB)
            imgB = Image.fromarray(imgB).resize((640,360),Image.ANTIALIAS)
            imgC = imageio.imread(image_nameC)
            imgC = Image.fromarray(imgC).resize((640,360),Image.ANTIALIAS)
            imgD = imageio.imread(image_nameD)
            imgD = Image.fromarray(imgD).resize((640,360),Image.ANTIALIAS)
            imgAB = np.concatenate([imgA, imgB], axis=1)
            imgCD = np.concatenate([imgC, imgD], axis=1)
            img = np.concatenate([imgAB, imgCD], axis=0)
            frames.append(img)
        else:
            print(image_nameA, image_nameB, ' no support!!')
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.5)
 
    return


def concatx6_create_gif(listA, listB, listC, listD, listE, listF, gif_name):
 
    frames = []
    for image_nameA, image_nameB, image_nameC, image_nameD, image_nameE, image_nameF in zip(listA, listB, listC, listD, listE, listF):
        if (image_nameA.endswith('.jpg') or image_nameA.endswith('.png')) and \
            (image_nameB.endswith('.jpg') or image_nameB.endswith('.png')):
            print(image_nameA, image_nameB)
            imgA = imageio.imread(image_nameA)
            imgA = Image.fromarray(imgA).resize((640,360),Image.ANTIALIAS)
            imgB = imageio.imread(image_nameB)
            imgB = Image.fromarray(imgB).resize((640,360),Image.ANTIALIAS)
            imgC = imageio.imread(image_nameC)
            imgC = Image.fromarray(imgC).resize((640,360),Image.ANTIALIAS)
            imgD = imageio.imread(image_nameD)
            imgD = Image.fromarray(imgD).resize((640,360),Image.ANTIALIAS)
            imgE = imageio.imread(image_nameE)
            imgE = Image.fromarray(imgE).resize((640,360),Image.ANTIALIAS)
            imgF = imageio.imread(image_nameF)
            imgF = Image.fromarray(imgF).resize((640,360),Image.ANTIALIAS)
            imgABC = np.concatenate([imgA, imgB, imgC], axis=1)
            imgDEF = np.concatenate([imgD, imgE, imgF], axis=1)
            img = np.concatenate([imgABC, imgDEF], axis=0)
            frames.append(img)
        else:
            print(image_nameA, image_nameB, ' no support!!')
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.5)



def get_imgs(path):
    image_list = os.listdir(path)
    image_list.sort()
    image_path_list=[os.path.join(path,img) for img in image_list]
    return image_path_list



def main():
 
    # 单个
    pathA='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/lidar/'
    pathC='/home/cidi/Workspace/bevfusion/runs/初步结果/'
    out_path = os.path.join(pathC, 'created_gif.gif')
    image_listA = os.listdir(pathA)
    image_listA.sort()
    image_path_listA=[pathA+img for img in image_listA]
    create_gif(image_path_listA, out_path)
    # ======

    # 两个
    # pathA='/home/cidi/Workspace/bevfusion/runs/初步结果/z_exp7_viz_cidi-byd_bevfusion_without-sweep_pred@cidi-byd_val/camera-1'
    # pathB='/home/cidi/Workspace/bevfusion/runs/初步结果/z_exp8_viz_cidi-byd_lidar-only_without-sweep_pred@cidi-byd_val/camera-1'
    # pathC='/home/cidi/Workspace/bevfusion/runs/初步结果/'
    # out_path = os.path.join(pathC, 'created_gif.gif')
    # image_listA = os.listdir(pathA)
    # image_listA.sort()
    # image_path_listA=[os.path.join(pathA,img) for img in image_listA]
    # image_listB = os.listdir(pathB)
    # image_listB.sort()
    # image_path_listB=[os.path.join(pathB,img) for img in image_listB]
    # assert len(image_path_listA)==len(image_path_listB), print(len(image_path_listA), len(image_path_listB))
    # concatx2_create_gif(image_path_listA, image_path_listB, out_path)
    # ==
 
    # 四个
    # pathA='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-0/'
    # pathB='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-3/'
    # pathC='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-1/'
    # pathD='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-2/'
    # path_out='/home/cidi/Workspace/bevfusion/runs/初步结果/'
    # out_path = os.path.join(path_out, 'created_gif.gif')
    # image_listA = os.listdir(pathA)
    # image_listA.sort()
    # image_path_listA=[os.path.join(pathA,img) for img in image_listA]
    # image_listB = os.listdir(pathB)
    # image_listB.sort()
    # image_path_listB=[os.path.join(pathB,img) for img in image_listB]
    # image_listC = os.listdir(pathC)
    # image_listC.sort()
    # image_path_listC=[os.path.join(pathC,img) for img in image_listC]
    # image_listD = os.listdir(pathD)
    # image_listD.sort()
    # image_path_listD=[os.path.join(pathD,img) for img in image_listD]
    # print(len(image_path_listA),len(image_path_listB),len(image_path_listC),len(image_path_listD))
    # assert len(image_path_listA)==len(image_path_listB), print(len(image_path_listA), len(image_path_listB))
    # concatx4_create_gif(image_path_listA, image_path_listB, image_path_listC, image_path_listD, out_path)
    # ==

    # 六个
    # pathA='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-2/'
    # pathB='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-0/'
    # pathC='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-1/'
    # pathD='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-4/'
    # pathE='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-3/'
    # pathF='/home/cidi/Workspace/bevfusion/runs/初步结果/viz/exp1_viz_nus_bevfusion_pred@nus-mini_val/camera-5/'
    # path_out='/home/cidi/Workspace/bevfusion/runs/初步结果/'
    # out_path = os.path.join(path_out, 'created_gif.gif')
    # image_path_listA=get_imgs(pathA)
    # image_path_listB=get_imgs(pathB)
    # image_path_listC=get_imgs(pathC)
    # image_path_listD=get_imgs(pathD)
    # image_path_listE=get_imgs(pathE)
    # image_path_listF=get_imgs(pathF)
    # print(len(image_path_listA),len(image_path_listB),len(image_path_listC),len(image_path_listD))
    # assert len(image_path_listA)==len(image_path_listB), print(len(image_path_listA), len(image_path_listB))
    # concatx6_create_gif(image_path_listA, image_path_listB, 
    #                     image_path_listC, image_path_listD, 
    #                     image_path_listE, image_path_listF,
    #                     out_path)


if __name__ == "__main__":
    main()