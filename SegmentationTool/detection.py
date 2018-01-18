import numpy as np
import SimpleITK as sitk
import cv2
def edge_detection(img,lower_thresh=0,upper_thresh=255):
    if isinstance(img,sitk.Image):
        canny_img = sitk.CannyEdgeDetection(sitk.Cast(img, sitk.sitkFloat32),
                        lowerThreshold=lower_thresh,
                        upperThreshold=upper_thresh,
                        variance=(0.05,0.05,0.05))
        return canny_img
    else:
        return None


def hough_cricle_detection(edge_image,minRadius=10,maxRadius=40):
    '''
    :param edge_image: 2D nd array image
    :return:image with circles,circles
    '''

    edge_image=np.uint8(edge_image)
    circles = cv2.HoughCircles(edge_image,cv2.HOUGH_GRADIENT,4, 260, param1=30, param2=65, minRadius=minRadius, maxRadius=maxRadius)
    new_circles = None
    if circles is not None:
        print 'success'
        new_circles = []
        # print 'success'
        # Convert the (x,y) coordinate and radius of the circles
        circles = np.round(circles[0, :]).astype("int")
        # Loop over the  (x,y) coordinate and radius of the circles
        for (x, y, r) in circles:
                if edge_image[y,x]>0:# roi center must be bright
                    new_circles.append((x, y, r))
                    cv2.circle(edge_image, (x, y), r, (100, 255, 0), 4)
    return edge_image,new_circles

if __name__=='__main__':
    import matplotlib.pyplot as plt
    from skimage.morphology import remove_small_objects
    img = cv2.imread('/mnt/data2/FW_Coronary/preprocess_result/11698661_BestSyst42%/11698661_BestSyst42%_15.jpg', 0)
    img=remove_small_objects(img,min_size=2000)
    edge_image,circles=hough_cricle_detection(img,40,100)

    plt.imshow(edge_image)
    plt.show()

