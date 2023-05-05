from fileinput import filename
import glob
import shutil
import cv2
import os
import numpy as np


def flip_img(path_):

    files = glob.glob(os.path.join(path_, '*.jpg'))
    files = files[:]
    print(len(files))
    out_dir = '/home/cidi/Datasets/pcd_img_database/2022-11-09_bkjw_标定/image'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for idx, fpath in enumerate(files):
        print(idx)
        img = cv2.imread(fpath)
        img = cv2.flip(img, -1) #原图顺时针旋转180度
        fname = os.path.split(fpath)[-1]
        out_path = os.path.join(out_dir,fname)
        cv2.imwrite(out_path, img)

    print('done!')



def pick_img(path_):

    #棋盘格模板规格
    w = 7
    h = 5

    files = glob.glob(os.path.join(path_, '*.jpg'))
    files = files[:]
    print(len(files))
    out_dir = '/home/cidi/Datasets/pcd_img_database/2022-11-09_bkjw_标定/good_images'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for idx, fpath in enumerate(files):
        print(idx)
        img = cv2.imread(fpath)
        img = cv2.flip(img, -1) #原图顺时针旋转180度
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray',gray)
        # cv2.waitKey(0)
        # 找到棋盘格角点
        ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
        if ret:
            print(ret)
            fname = os.path.split(fpath)[-1]
            out_path = os.path.join(out_dir,fname)
            shutil.copy(fpath,out_path)

    print('done!')


def main(path_):

    # 阈值
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    #棋盘格模板规格
    w = 7
    h = 5
    # 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
    objp = np.zeros((w*h,3), np.float32)
    objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
    # 储存棋盘格角点的世界坐标和图像坐标对
    objpoints = [] # 在世界坐标系中的三维点
    imgpoints = [] # 在图像平面的二维点


    files = glob.glob(os.path.join(path_, '*.jpg'))
    files = files[:]
    print(len(files))
    save_dir = '/home/cidi/Datasets/pcd_img_database/2022-11-09_bkjw_标定/done_images'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    for idx, fpath in enumerate(files):
        print(idx)
        img = cv2.imread(fpath)
        img = cv2.flip(img, -1) #原图顺时针旋转180度
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 找到棋盘格角点
        ret, corners = cv2.findChessboardCorners(gray, (w,h), None)
        # 如果找到足够点对，将其存储起来
        if ret == True:
            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            objpoints.append(objp)
            imgpoints.append(corners)
            # 将角点在图像上显示
            cv2.drawChessboardCorners(img, (w,h), corners, ret)
            fname = os.path.split(fpath)[-1]
            save_path = os.path.join(save_dir,fname)
            cv2.imwrite(save_path, img)
            # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print (("ret:"),ret)
    print (("mtx:\n"),mtx)        # 内参数矩阵
    print (("dist:\n"),dist)      # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)
    # print (("rvecs:\n"),rvecs)    # 旋转向量  # 外参数
    # print (("tvecs:\n"),tvecs)    # 平移向量  # 外参数
    # 去畸变
    one_file = files[0]
    img2 = cv2.imread(one_file)
    img2 = cv2.flip(img2, -1) #原图顺时针旋转180度
    h,w = img2.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h)) # 自由比例参数
    dst = cv2.undistort(img2, mtx, dist, None, newcameramtx)
    # 根据前面ROI区域裁剪图片
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    fname = os.path.split(one_file)[-1]
    save_path = os.path.join(save_dir,fname+'_calibresult.jpg')
    cv2.imwrite(save_path, dst)

    # 反投影误差
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        total_error += error
    print (("total error: "), total_error/len(objpoints))


if __name__=='__main__':
    flip_img('/home/cidi/Datasets/pcd_img_database/2022-11-09_bkjw_标定/ori_images/')
    # pick_img('/home/cidi/Datasets/pcd_img_database/2022-11-09_bkjw_标定/image/')
    # main('/home/cidi/Datasets/pcd_img_database/2022-11-09_bkjw_标定/good_images/')