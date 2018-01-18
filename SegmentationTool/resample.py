import numpy as np
import SimpleITK as sitk


def resample_by_spacing(im, new_spacing, interpolator=sitk.sitkLinear):
    scaling = np.array(new_spacing) / np.array(im.GetSpacing())
    new_size = (np.array(im.GetSize()) / scaling).astype("int")
    transform = sitk.AffineTransform(3)
    transform.SetCenter(im.GetOrigin())
    return sitk.Resample(im, new_size, transform, interpolator, im.GetOrigin(), new_spacing, im.GetDirection())


def resample_by_ref(im, refim, interpolator=sitk.sitkLinear):
    transform = sitk.AffineTransform(3)
    transform.SetCenter(im.GetOrigin())
    return sitk.Resample(im, refim, transform, interpolator)