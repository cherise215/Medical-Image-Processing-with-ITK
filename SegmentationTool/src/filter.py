import numpy as np
import SimpleITK as sitk
import cv2
from skimage.filters import frangi, hessian
import itk

def adaptive_thresh(img, percentage=98):
    '''
    percentage enhancement
    :param img: 3D sitk image
    :param percentage:
    :return:
    '''
    a = sitk.GetArrayFromImage(img)
    b = sitk.GetArrayFromImage(sitk.Median(img, (3, 3, 3)))

    top = np.percentile(a.ravel(), percentage)

    # replace only voxels in 98th or higher percentile
    # with median smoothed value
    a[a > top] = b[a > top]
    a = sitk.GetImageFromArray(a)
    a.CopyInformation(img)
    return a


def smooth_image(sitk_im_series,variance=0.5):
    '''
    3D sitk image
    :param sitk_im_series:
    :param variance:
    :return:
    '''
    gaussian = sitk.DiscreteGaussianImageFilter()
    gaussian.SetVariance(variance)
    gaussian_im = gaussian.Execute(sitk_im_series)
    return gaussian_im

def curvature_flow_smooth(sitk_im_series,time_step=0.125,number_of_iterations=5):
    img_smooth = sitk.CurvatureFlow(image1=sitk_im_series,
                                          timeStep=time_step,
                                          numberOfIterations=number_of_iterations)
    return img_smooth

def blur_image(sitk_im_series):
    '''
    blur_image on 3D sitk image series
    :param sitk_im_series:
    :return:
    '''
    blurFilter = sitk.CurvatureFlowImageFilter()
    blurFilter.SetNumberOfIterations(1)
    blurFilter.SetTimeStep(0.125)
    blur_image = blurFilter.Execute(sitk_im_series)
    return blur_image

def close_boundary(mask):
    '''
    close_boundary on 3D sitk image series

    :param mask:
    :return:
    '''
    boundary = sitk.BinaryMorphologicalClosing(mask, 2)
    # Remove any label pixel not connected to the boarder
    mask = sitk.BinaryGrindPeak(boundary)
    return mask

def CLAHE(image,clipLimit=2.0,tileGridSize=(8,8)):
    '''
    adaptive histogram equalization
    locally contrast enhancement based on histogram equalization
    input 2D array (M,N) M*N image
    return contrast image
    :param image: 2D image (nd array)
    :return:
    '''
    clahe = cv2.createCLAHE(clipLimit=clipLimit,tileGridSize=tileGridSize)
    cl_image=clahe.apply(image)
    return cl_image

def equal_hist(image):
    from skimage.exposure import equalize_hist
    equalized_image = equalize_hist(image)
    return  equalized_image

def frangi_enhancement(image,scale_range=(1,10), scale_step=2,beta1=0.5,beta2=15,black_ridges=False):
    '''
    This filter can be used to detect continuous edges on a 2D image
    e.g. vessels, wrinkles, rivers. It can be used to calculate the fraction of the whole image containing such objects.
    :param image:
    :param scale_range:The range of sigmas used. A larger Sigma will decrease the identification of noise or small structures as vessels.
    :param scale_step:float, optional Step size between sigmas.
    :param beta1:float, optional
    :param beta2:beta2 : float, optional
    :param black_ridges: the filter detects black ridges; when False, it detects white ridges.
    :return:
    '''

    result=frangi(image,scale_range=scale_range,scale_step=scale_step,beta1=beta1,beta2=beta2,black_ridges=black_ridges)
    return result



