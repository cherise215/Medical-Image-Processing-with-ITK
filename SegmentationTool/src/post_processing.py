from skimage.segmentation import clear_border
def  clear_border(labels, buffer_size=0, bgval=0):
    '''
    labels: (M[, N[, ..., P]]) array of int or bool
        Imaging data labels.
    :param labels:
    :param buffer_size:
        int, optional
        The width of the border examined.  By default, only objects
        that touch the outside of the image are removed.
    :param bgval: float or int, optional, Cleared objects are set to this value.
    :param in_place:bool        Whether or not to manipulate the labels array in-place.
    :return:
    '''
    clear_border(labels, buffer_size, bgval, in_place=True)
    return labels


