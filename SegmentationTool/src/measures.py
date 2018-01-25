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

def cal_overlapping_ratio(detection_1, detection_2):
    '''
    Function to calculate overlapping area'si
    `detection_1` and `detection_2` are 2 detections whose area
    of overlap needs to be found out.
    Each detection is list in the format ->
    [x-top-left, y-top-left, width-of-detection, height-of-detection]
    The function returns a value between 0 and 1,
    which represents the area of overlap.
    0 is no overlap and 1 is complete overlap.
    Area calculated from ->
    http://math.stackexchange.com/questions/99565/simplest-way-to-calculate-the-intersect-area-of-two-rectangles
    '''
    # Calculate the x-y co-ordinates of the
    # rectangles
    x1_tl = detection_1[0]
    x2_tl = detection_2[0]
    x1_br = detection_1[0] + detection_1[2]
    x2_br = detection_2[0] + detection_2[2]
    y1_tl = detection_1[1]
    y2_tl = detection_2[1]
    y1_br = detection_1[1] + detection_1[3]
    y2_br = detection_2[1] + detection_2[3]
    # Calculate the overlapping Area
    x_overlap = max(0, min(x1_br, x2_br)-max(x1_tl, x2_tl))
    y_overlap = max(0, min(y1_br, y2_br)-max(y1_tl, y2_tl))
    overlap_area = x_overlap * y_overlap
    area_1 = detection_1[2] * detection_2[3]
    area_2 = detection_2[2] * detection_2[3]
    total_area = area_1 + area_2 - overlap_area
    return overlap_area / float(total_area)