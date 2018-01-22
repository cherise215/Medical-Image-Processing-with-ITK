import SimpleITK as sitk

def getMinMax( img):
    mm = sitk.MinimumMaximumImageFilter()
    mm.Execute(img)
    return (mm.GetMinimum(), mm.GetMaximum())

def getStatistic(img):
    image_statistic = sitk.StatisticsImageFilter()
    statistic = image_statistic.Execute(img)
    return statistic
