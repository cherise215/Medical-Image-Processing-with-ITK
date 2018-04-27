import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import exposure

def get_hog_feature(image,orientation=9,pixels_per_cell=16,cells_per_block=1,if_visualise=True,if_transform_sqrt=True):
    fd, hog_image = hog(image, orientations=orientation, pixels_per_cell=(pixels_per_cell, pixels_per_cell),
                        cells_per_block=(cells_per_block, cells_per_block), block_norm='L2-Hys',transform_sqrt=if_transform_sqrt, visualise=if_visualise)

    return fd,hog_image




if __name__ == '__main__':
    import dicom
    dcm=dicom.read_file('/mnt/data2/FW_Coronary/2017_12_26_houzhihui_29/dcm/11698641_BestDiast70%/BJFW11698641S5_001.dcm')
    image=dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
    fd,hog_image=get_hog_feature(image)
    print (hog_image.shape)
    import numpy as np
    #print np.sqrt(fd.shape[0])
    #visualize
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

    ax1.axis('off')
    ax1.imshow(image, cmap=plt.cm.gray)
    ax1.set_title('Input image')
    ax1.set_adjustable('box-forced')

    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
    ax2.set_title('Histogram of Oriented Gradients')
    ax1.set_adjustable('box-forced')
    plt.show()