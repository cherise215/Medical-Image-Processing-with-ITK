import itk

def read_dicom_series(patient_dir):
    '''
    given a image dir
    return itk image
    :param patient_dir:
    :return:
    '''
    input_pixel_type = itk.ctype('float')
    image_type = itk.Image[input_pixel_type, 3]
    reader = itk.ImageSeriesReader[image_type].New()
    gdcm_io = itk.GDCMImageIO.New()
    reader.SetImageIO(gdcm_io)
    names_generator = itk.GDCMSeriesFileNames.New()
    names_generator.SetInputDirectory(patient_dir)
    file_names = names_generator.GetInputFileNames()
    reader.SetFileNames(file_names)
    try:
        reader.Update()
    except:
        raise
    return reader.GetOutput()
