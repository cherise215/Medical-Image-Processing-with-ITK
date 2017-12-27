
# coding: utf-8


import os 
import itk
import dicom
import numpy as np
import SimpleITK as sitk
import time
import collections


#use decorator to calculate func time
def show_time(func):
    def _deco(*args, **kwargs):
        st = time.clock()
        result=func(*args, **kwargs)
        et = time.clock()
        delta = et - st
        print 'call %s() used %fs' % (func.__name__, delta)
        return result
    return _deco

# decompress dicom series
def decompress(img_dir):
    for dcm in os.listdir(img_dir):
        dcm = os.path.join(img_dir,dcm)
        cmd = 'gdcmconv -w ' + dcm + ' ' + dcm
        os.system(cmd)

@show_time
def read_dcm_by_itk(patient_dir):
    '''
    using ITK to load dicom series after Hu transform
    :param patient_dir: directory. e.g dicom_dir
    :return: image nd narray [N*H*W]
    '''
    pixel_type = itk.ctype('signed short')
    internal_image_type = itk.Image[pixel_type, 3]
    reader = itk.ImageSeriesReader[internal_image_type].New()
    
    gdcm_io=itk.GDCMImageIO.New()
    reader.SetImageIO(gdcm_io)
    
    names_generator=itk.GDCMSeriesFileNames.New()
    names_generator.SetInputDirectory(patient_dir)    
    file_names=names_generator.GetInputFileNames()
    reader.SetFileNames(file_names)
    
    try:
        reader.Update()
    except:
        raise
    im=reader.GetOutput()
    nd_array=itk.GetArrayFromImage(im)
    return nd_array
    
@show_time   
def read_dcm_by_simple_itk(patient_dir):
    '''
    using SimpleITK to load dicom series after Hu transform
    :param patient_dir: directory. e.g dicom_dir
    :return: image nd narray [N*H*W]
    '''
    assert os.path.isdir(patient_dir), '%s not a valid directory' % patient_dir
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(patient_dir)
    
    reader.SetFileNames(dicom_names)
    im = reader.Execute()
    image_nd_array = sitk.GetArrayFromImage(im)
    return image_nd_array


@show_time
def read_dcm_by_dicom(patient_dir):
    '''
     using dicom package to read dcm
    :param patient_dir: directory. e.g dicom_dir
    :return: image nd narray [N*H*W]
    '''
    assert os.path.isdir(patient_dir), '%s not a valid directory' % patient_dir
    # read dicom objects 
    dcm_list = [dicom.read_file(os.path.join(patient_dir,i),force=True)
                for i in sorted(os.listdir(patient_dir))]
    
    assert len(dcm_list)>0, 'No dicom has been loaded under %s'  %patient_dir
    
    # extract image data
    try:
        image_volume_array = np.stack([dcm.pixel_array for dcm in dcm_list])
    except :
        decompress(patient_dir)
        image_volume_array = np.stack([dcm.pixel_array for dcm in dcm_list])
        
    
    # Hough Unit
    rescale_slope = 1
    rescale_slope = 0
    try:
        rescale_slope = dcm_list[0].RescaleSlope
        rescale_intercept = dcm_list[0].RescaleIntercept
    except NotImplementedError:
        raise
    
    if not rescale_slope is 1:
        image_volume_array = rescale_slope * image_volume_array.astype(np.float64)
        image_volume_array = image_volume_array.astype(np.int16)
    
    if not rescale_intercept is 0:
        image_volume_array += np.int16(rescale_intercept)
   
    #print image_volume_array.shape
    return image_volume_array
      
if __name__=='__main__':
    # compare test time

	patient_dir='CT/SRS00002'

	dicom_img_array = read_dcm_by_dicom(patient_dir)  # read according to filename orders, usually read from head to foot.
	sitk_img_array= read_dcm_by_simple_itk(patient_dir) # read direction: from foot to head
	itk_img_array=read_dcm_by_itk(patient_dir)  #read direction from foot to head


    #import matplotlib.pyplot as plt
    # plt.imshow(dicom_img_array[110])


    

