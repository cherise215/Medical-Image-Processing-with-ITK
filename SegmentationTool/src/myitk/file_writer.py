import itk
def write_imageseries(itk_img,file_path):
    input_pixel_type = itk.ctype('float')
    image_type = itk.Image[input_pixel_type, 3]
    writer = itk.ImageFileWriter[image_type].New()

    writer.SetInput(itk_img)
    writer.SetFileName(file_path)
    writer.Update()
