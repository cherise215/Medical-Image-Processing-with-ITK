import numpy as np
import SimpleITK as sitk
import cv2
from skimage.feature import corner_harris, corner_peaks
def edge_detection(img,lower_thresh=0,upper_thresh=255):
    if isinstance(img,sitk.Image):
        canny_img = sitk.CannyEdgeDetection(sitk.Cast(img, sitk.sitkFloat32),
                        lowerThreshold=lower_thresh,
                        upperThreshold=upper_thresh,
                        variance=(0.05,0.05,0.05))
        return canny_img
    else:
        return None


def corner_detection(img,min_distance=1):
    corner_points=corner_peaks(corner_harris(img), min_distance=min_distance)
    return  corner_points

def AO_cricle_detection(edge_image,minRadius=10,maxRadius=40):
    '''
    :param edge_image: 2D nd array image
    :return:image with circles,circles
    '''

    edge_image=np.uint8(edge_image)
    circles = cv2.HoughCircles(edge_image,cv2.HOUGH_GRADIENT,4, 260, param1=30, param2=65, minRadius=minRadius, maxRadius=maxRadius)
    new_circles = None
    if circles is not None:
        print ('success')
        new_circles = []
        # print 'success'
        # Convert the (x,y) coordinate and radius of the circles
        circles = np.round(circles[0, :]).astype("int")
        # Loop over the  (x,y) coordinate and radius of the circles
        for (x, y, r) in circles:
                if edge_image[y,x]>0 and x<y and  x<200:# aota in the left upper domain,roi center must be bright
                    print (x,y)
                    new_circles.append((x, y, r))
                    cv2.circle(edge_image, (x, y), r, (100, 255, 0), 4)
    return edge_image,new_circles

def hough_cricle_detection(edge_image,minRadius=10,maxRadius=40):
    '''
    :param edge_image: 2D nd array image
    :return:image with circles,circles
    '''

    edge_image=np.uint8(edge_image)
    circles = cv2.HoughCircles(edge_image,cv2.HOUGH_GRADIENT,4, 260, param1=30, param2=65, minRadius=minRadius, maxRadius=maxRadius)
    new_circles = None
    if circles is not None:
        print ('success')
        new_circles = []
        # print 'success'
        # Convert the (x,y) coordinate and radius of the circles
        circles = np.round(circles[0, :]).astype("int")
        # Loop over the  (x,y) coordinate and radius of the circles
        for (x, y, r) in circles:
            new_circles.append((x, y, r))
            cv2.circle(edge_image, (x, y), r, (100, 255, 0), 4)
    return edge_image,new_circles

def template_matching(img,template,method,if_draw=False):
    method=cv2.TM_CCOEFF_NORMED
    img=np.uint8(img).copy()
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    w,h = template.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if if_draw:
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
    center=((top_left[0] + w/2.0),(top_left[1]+h/2.0))
    return w,h,center,img

if __name__=='__main__':
    import matplotlib.pyplot as plt
    from skimage.morphology import remove_small_objects
    img = cv2.imread('/mnt/data2/FW_Coronary/preprocess_result/11698661_BestSyst42%/11698661_BestSyst42%_15.jpg', 0)
    img=remove_small_objects(img,min_size=2000)
    edge_image,circles=hough_cricle_detection(img,40,100)

    plt.imshow(edge_image)
    plt.show()

