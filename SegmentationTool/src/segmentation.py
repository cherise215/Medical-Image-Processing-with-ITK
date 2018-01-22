import SimpleITK as sitk

def chan_vess_segmentation(image):
    '''
    input sitk image type 3D series
    '''
    thres = sitk.MomentsThresholdImageFilter()
    thres.SetNumberOfHistogramBins(128)
    thres.SetInsideValue(0)
    thres.SetOutsideValue(1)
    res = thres.Execute(image)
    phi0 = sitk.SignedMaurerDistanceMap(res,insideIsPositive=False,squaredDistance=False,useImageSpacing=True)
    vessel_filter=sitk.ScalarChanAndVeseDenseLevelSetImageFilter()
    vessel_filter.SetLambda1(1)
    vessel_filter.SetLambda2(1)
    vessel_filter.UseImageSpacingOn()
    vessel_filter.SetHeavisideStepFunction(0)
    vessel_filter.SetCurvatureWeight(0.0)
    vessel_filter.SetNumberOfIterations(3)
    result=vessel_filter.Execute(phi0,sitk.Cast(image,sitk.sitkFloat32))
    mask= sitk.BinaryThreshold(result, 1e-7, 1e7)
    return mask

def otsu_segmentation(image,num_bins=2,valley_emphasis=False):
    '''

    :param img: sitk image type 3D series
    :param num_bins: int
    :param valley_emphasis:
    :return:
    '''
    otsu_filter = sitk.OtsuMultipleThresholdsImageFilter()
    otsu_filter.SetNumberOfHistogramBins(num_bins)
    otsu_filter.SetValleyEmphasis(valley_emphasis)
    mask=otsu_filter.Execute(image)
    thresh=otsu_filter.GetThresholds()
    return [mask,thresh]


def moment_segmentation(image, num_bins=128):
    thres = sitk.MomentsThresholdImageFilter()
    thres.SetNumberOfHistogramBins(num_bins)
    thres.SetInsideValue(0)
    thres.SetOutsideValue(1)
    mask = thres.Execute(image)
    thresh = thres.GetThreshold()
    return [mask,thresh]


def kmeans_segmentation(image, initial_mean=[30,100,20]):
    kmeans_filter = sitk.ScalarImageKmeansImageFilter()
    kmeans_filter.SetClassWithInitialMean(initial_mean)
    result=kmeans_filter.Execute(image)
    means=kmeans_filter.GetFinalMeans()
    return [result,means]

def region_grow_by_neighborhood(image,seed_list,radius=5,lower_thresh=0,upper_thresh=255):

    neibour = sitk.NeighborhoodConnectedImageFilter()
    neibour.SetRadius(radius)
    neibour.SetLower(lower_thresh)
    neibour.SetUpper(upper_thresh)
    neibour.SetSeedList(seed_list)
    mask = neibour.Execute(image)
    #mask = sitk.BinaryDilate(mask, 4)

    return mask

def  region_grow_implicit(image,seed_list,lower_thresh,upper_thresh):
    seg = sitk.BinaryThreshold(image, lowerThreshold=lower_thresh,
                               upperThreshold=upper_thresh, insideValue=1, outsideValue=0)
    seg = sitk.BinaryDilate(seg, 2)
    seg_implicit_thresholds = sitk.ConfidenceConnected(seg, seedList=seed_list,
                                                       numberOfIterations=0,
                                                       multiplier=5,
                                                       initialNeighborhoodRadius=1,
                                                       replaceValue=1)
    return seg_implicit_thresholds

def  region_grow_explicit(image,seed_list,lower_thresh,upper_thresh):
    seg_explicit_thresholds = sitk.ConnectedThreshold(image, seedList=seed_list, lower=lower_thresh, upper=upper_thresh)

    #closing
    mask=sitk.BinaryErode(sitk.BinaryDilate(seg_explicit_thresholds, 5), 5)

    return mask

