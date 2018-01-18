import os
import SimpleITK as sitk
import cv2
import time

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

def read_dcm_by_simple_itk(patient_dir,window_center=300,window_width=800):
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
    im=im[:,:,::-1]
    im_255 = sitk.IntensityWindowing(im,window_center-window_width//2,window_center+window_width//2,0,255)
    im_255 =sitk.Cast(im_255,sitk.sitkUInt8)
    return [im,im_255]

def save_files(image, save_dir=None,file_nameprefix=None,ext='.jpg'):
    '''
    write series image into a save dir
    :param image: support sitk image type, ndarray and list of images
    :param save_dir: dir for saving
    :param file_nameprefix: string
    :param ext: save image extension
    :return:
    '''
    if save_dir is None:
        save_dir='save/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if isinstance(image,sitk.Image):
        process_imgs=sitk.GetArrayFromImage(image)
        size=process_imgs.shape[0]
    elif isinstance(image,list):
        process_imgs=image
        size=len(process_imgs)
    else:
        assert len(image.shape)==3,'must be 3D array, N*H*W'
        process_imgs=image
        size = process_imgs.shape[0]
    file_prefix = os.path.split(os.path.abspath(save_dir))[-1] if file_nameprefix is None else file_nameprefix
    file_names=[file_prefix+'_'+str(i)+ext for i in range(size)]

    for i in range(size):
        im_slice=process_imgs[i]
        save_path=os.path.join(save_dir,file_names[i])
        cv2.imwrite(save_path,im_slice)

def  get_extact_slice(sitk_im_series,  index):
    '''
    extract a single slice from sitk_im_series
    :param sitk_im_series: sitk image series
    :param index: int
    :return: simple itk image
    '''
    im_size=sitk_im_series.GetSize()
    selected_slice = sitk.Extract(sitk_im_series, (im_size[0], im_size[1], 0), (0, 0, index))
    return selected_slice


def add_gaussian(img):
    '''
    add gaussian into a image
    :param img:
    :return:
    '''
    add = sitk.AddImageFilter()
    gaussian = sitk.GaussianSource(size=img.GetSize())
    gaussian.CopyInformation(img)
    gaussian_new = add.Execute(img, gaussian)
    return gaussian_new

def compose_image(img1,img2):
    '''
    compose two sitk images into one
    :param img1: sitk image 1
    :param img2: sitk image 2
    :return:
    '''
    compose_image=sitk.Compose(img1,img2)
    return compose_image