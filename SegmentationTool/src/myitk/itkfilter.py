import itk

def frangi_3D(itk_image,sigma,alpha1,alpha2):
    '''
    frangi_3D
    adapted from https://itk.org/ITKExamples/src/Filtering/ImageFeature/SegmentBloodVessels/Documentation.html
    :param itk_image:
    :param sigma: float
    :param alpha1: float
    :param alpha2: float
    :return:
    '''
    input_pixel_type = itk.ctype('float')
    input_image_type = itk.Image[input_pixel_type, 3]

    hessian_filter=itk.HessianRecursiveGaussianImageFilter[input_image_type].New()
    hessian_filter.SetInput(itk_image)
    hessian_filter.SetSigma(sigma )
    hessian_filter.Update()

    vesselness_filter = itk.Hessian3DToVesselnessMeasureImageFilter[input_pixel_type].New()
    vesselness_filter.SetInput(hessian_filter.GetOutput())

    vesselness_filter.SetAlpha1(alpha1)
    vesselness_filter.SetAlpha2(alpha2)
    vesselness_filter.Update()
    result=vesselness_filter.GetOutput()

    return result

def laplacian_recursive_gaussian_filter(image):
    '''
    reference: C++ version https://itk.org/ITKExamples/src/Filtering/ImageFeature/LaplacianRecursiveGaussianImageFilter/Documentation.html
    :param image: itk 3D image
    :return: itk 3D image
    '''
    input_pixel_type = itk.ctype('float')
    input_image_type = itk.Image[input_pixel_type, 3]
    filter=itk.LaplacianRecursiveGaussianImageFilter[input_image_type,input_image_type].New()
    filter.SetInput(image)
    filter.Update()
    result = filter.GetOutput()
    # rescale_filter = itk.RescaleIntensityImageFilter[input_image_type,input_image_type].New()
    # rescale_filter.SetInput(result)
    # outputPixelTypeMinimum = itk.NumericTraits[input_image_type].min()
    # outputPixelTypeMaximum = itk.NumericTraits[input_image_type].max()
    #
    #
    return  result



def sobel_filter(image):
    '''
    reference: C++ version https://itk.org/ITKExamples/src/Filtering/ImageFeature/SobelEdgeDetectionImageFilter/Documentation.html
    :param image: itk 3D image
    :return: itk 3D image
    '''
    input_pixel_type = itk.ctype('float')
    input_image_type = itk.Image[input_pixel_type, 3]
    filter=itk.SobelEdgeDetectionImageFilter[input_image_type,input_image_type].New()
    filter.SetInput(image)
    filter.Update()
    result = filter.GetOutput()

    return  result




def canny_filter(image,variance,lower_threshold,upper_threshold):
    '''
    reference: C++ version https://itk.org/ITKExamples/src/Filtering/ImageFeature/SobelEdgeDetectionImageFilter/Documentation.html
    This filter is an implementation of a Canny edge detector for scalar-valued images.
    :param image: itk 3D image
    :param variance:Variance are used in the Gaussian smoothing
    :param lower_threshold:lower_threshold is the lowest allowed value in the output image.
    :param upper_threshold: values below the Threshold level will be replaced with the OutsideValue parameter value, whose default is zero.
    :return:itk 3D image
    '''

    input_pixel_type = itk.ctype('float')
    input_image_type = itk.Image[input_pixel_type, 3]
    filter=itk.CannyEdgeDetectionImageFilter[input_image_type,input_image_type].New()
    filter.SetInput(image)
    filter.SetVariance(variance)
    filter.SetLowerThreshold(lower_threshold)
    filter.SetUpperThreshold(upper_threshold)
    filter.Update()
    result = filter.GetOutput()

    return  result




