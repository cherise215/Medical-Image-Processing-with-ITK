import numpy as np
import SimpleITK as sitk
import cv2
def cal_distance(point_1,point_2):
    '''
    calculate distance between two points
    :param point_1:  tuple of 2 float : e.g.(11,10)
    :param point_2: tuple of 2 float : e.g.(11,10)
    :return: double float: distance of two point
    '''
    squared_dist=np.sum((np.array(point_1)-np.array(point_2))**2)
    std_dist=np.sqrt(squared_dist)
    return std_dist

def  cal_optical_flow(sitk_im_series,start_index,end_index):
    '''

    :param sitk_im_series: sitk image series
    :param start_index: start index
    :param end_index: endindex
    :return: optical flow image
    '''
    im_size=sitk_im_series.GetSize()
    prev_img= sitk.GetArrayFromImage(sitk.Extract(sitk_im_series, (im_size[0], im_size[1], 0), (0, 0, start_index)))
    cur_img= sitk.GetArrayFromImage(sitk.Extract(sitk_im_series, (im_size[0], im_size[1], 0), (0, 0, end_index)))
    image=cv2.calcOpticalFlowFarneback(prev_img, cur_img,cur_img-prev_img,pyr_scale=0.5,levels=1,winsize=5,iterations=10,poly_n=1,poly_sigma=0.5,flags=1)
    return  image