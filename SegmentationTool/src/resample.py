import numpy as np
import SimpleITK as sitk


def resample_by_spacing(im, new_spacing, interpolator=sitk.sitkLinear):
    '''
    resample by image spacing
    :param im: sitk image
    :param new_spacing: new image spa
    :param interpolator: sitk.sitkLinear, sitk.NearestNeighbor
    :return:
    '''
    scaling = np.array(new_spacing) / np.array(im.GetSpacing())
    new_size = (np.array(im.GetSize()) / scaling).astype("int")
    transform = sitk.AffineTransform(3)
    transform.SetCenter(im.GetOrigin())
    return sitk.Resample(im, new_size, transform, interpolator, im.GetOrigin(), new_spacing, im.GetDirection())


def resample_by_ref(im, refim, interpolator=sitk.sitkLinear):

    transform = sitk.AffineTransform(3)
    transform.SetCenter(im.GetOrigin())
    return sitk.Resample(im, refim, transform, interpolator)


def MIP(im,start_index,end_index):
    '''
    maxium intensity projection
    :param im:
    :param start_index:
    :param end_index:
    :return:
    '''
    if isinstance(im,sitk.Image):
        arr=sitk.GetArrayFromImage(im)
    else:
        arr=im
    blob_image = arr[start_index:end_index]
    n, h, w = arr.shape
    best = np.argmax(blob_image, 0)
    blob_slice_number = end_index - start_index
    blob_image = blob_image.reshape((blob_slice_number, -1))  # image is now (blob_slice_number, nr_pixels)
    blob_image = blob_image.transpose()  # image is now (nr_pixels, stack)
    rebuild_2 = blob_image[np.arange(len(blob_image)), best.ravel()]  # Select the right pixel at each location
    rebuild_2 = rebuild_2.reshape((h, w))
    return rebuild_2

