import numpy as np
import SimpleITK as sitk



def adaptive_thresh(img, percentage=98):
    '''

    :param img: sitk image
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


def  smooth_image(sitk_im_series,variance=0.5):
    gaussian = sitk.DiscreteGaussianImageFilter()
    gaussian.SetVariance(variance)
    gaussian_im = gaussian.Execute(sitk_im_series)
    return gaussian_im

def  blur_image(sitk_im_series):
    blurFilter = sitk.CurvatureFlowImageFilter()
    blurFilter.SetNumberOfIterations(1)
    blurFilter.SetTimeStep(0.125)
    blur_image = blurFilter.Execute(sitk_im_series)
    return blur_image

def close_boundary(mask):
    boundary = sitk.BinaryMorphologicalClosing(mask, 2)
    # Remove any label pixel not connected to the boarder
    mask = sitk.BinaryGrindPeak(boundary)
    return mask
