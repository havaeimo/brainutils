import itk
import os
import numpy
import numpy as np
import argparse
import pdb
import nibabel as nib
from os.path import join


def convert_mhd_2_mha(data_filepath, output_filepath):
    image_type_read = itk.Image[itk.SS, 3]

    itk_py_converter_read = itk.PyBuffer[image_type_read]

    reader = itk.ImageFileReader[image_type_read].New()
    reader.SetFileName(data_filepath)
    reader.Update()

    read = reader.GetOutput()

    T1 = itk_py_converter_read.GetArrayFromImage(read)

    T1 = np.asarray(T1, dtype=int)
    image_type_write = itk.Image[itk.SS, 3]

    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist())
    itk_image.SetSpacing(read.GetSpacing())
    itk_image.SetOrigin(read.GetOrigin())
    itk_image.SetDirection(read.GetDirection())
    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()
    del writer
    del reader
    del itk_image


def convert_nii_2_mha(data_filepath, ref_filepath, output_filepath):  # for use for cuda2. orientation should be RAI

    image_type_read = itk.Image[itk.SS, 3]
    image_type_ref = itk.Image[itk.SS, 3]

    itk_py_converter_read = itk.PyBuffer[image_type_read]
    itk_py_converter_ref = itk.PyBuffer[image_type_ref]

    reader = itk.ImageFileReader[image_type_read].New()
    ref = itk.ImageFileReader[image_type_ref].New()
    # pdb.set_trace()
    reader.SetFileName(data_filepath)
    reader.Update()

    ref.SetFileName(ref_filepath)
    ref.Update()

    out = reader.GetOutput()
    reference = ref.GetOutput()

    T1 = itk_py_converter_read.GetArrayFromImage(out)
    T1 = T1[:, ::-1, ::-1]
    #assert T1.flatten().max == 1
    #T1 = (T1 / T1.flatten().max()) * 255
    T1 = np.asarray(T1, dtype=int)
    image_type_write = itk.Image[itk.SS, 3]

    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist())
    itk_image.SetSpacing(reference.GetSpacing())
    itk_image.SetOrigin([131.1, 132.3, -44.76])
    # itk_image.SetDirection(reference.GetDirection())
    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()
    del writer
    del reader
    del itk_image


def changeheader_mha(data_filepath, ref_filepath, output_filepath):
    from ipdb import set_trace
    set_trace()
    image_type_read = itk.Image[itk.SS, 3]
    image_type_ref = itk.Image[itk.SS, 3]

    itk_py_converter_read = itk.PyBuffer[image_type_read]
    itk_py_converter_ref = itk.PyBuffer[image_type_ref]

    reader = itk.ImageFileReader[image_type_read].New()
    ref = itk.ImageFileReader[image_type_ref].New()
    # pdb.set_trace()
    reader.SetFileName(data_filepath)
    reader.Update()

    ref.SetFileName(ref_filepath)
    ref.Update()

    out = reader.GetOutput()
    reference = ref.GetOutput()

    T1 = itk_py_converter_read.GetArrayFromImage(out)
    T1 = T1[:, ::-1, ::-1]
    #assert T1.flatten().max == 1
    #T1 = (T1 / T1.flatten().max()) * 255
    T1 = np.asarray(T1, dtype=int)
    image_type_write = itk.Image[itk.SS, 3]

    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist())
    itk_image.SetSpacing(reference.GetSpacing())
    itk_image.SetOrigin([131.1, 132.3, -44.76])
    itk_image.SetDirection(reference.GetDirection())
    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()
    del writer
    del reader
    del itk_image


def nii2mha_int(data_filepath, output_filepath):

    image_type_read = itk.Image[itk.F, 3]
    itk_py_converter_read = itk.PyBuffer[image_type_read]
    reader = itk.ImageFileReader[image_type_read].New()
    # pdb.set_trace()
    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    T1 = itk_py_converter_read.GetArrayFromImage(out)
    T1 = T1[:, ::-1, ::-1]
    #assert T1.flatten().max == 1
    T1 = (T1 / T1.flatten().max()) * 255
    T1 = np.asarray(T1, dtype=int)
    image_type_write = itk.Image[itk.SS, 3]
    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist())
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(0)

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()
    del writer
    del reader
    del itk_image


def nii2mha_label(data_filepath, output_filepath):

    image_type_read = itk.Image[itk.F, 3]
    itk_py_converter_read = itk.PyBuffer[image_type_read]
    reader = itk.ImageFileReader[image_type_read].New()
    # pdb.set_trace()
    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    T1 = itk_py_converter_read.GetArrayFromImage(out)
    T1 = T1[:, ::-1, ::-1]
    #assert T1.flatten().max == 1
    #T1 = (T1/T1.flatten().max())*255
    T1 = np.asarray(T1, dtype=int)
    image_type_write = itk.Image[itk.SS, 3]
    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)

    itk_image = itk_py_converter_write.GetImageFromArray(T1.tolist())
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(0)

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()


def merge_nii(path_read, tensor_path):
    import os
    dir_list = [join(path_read, f) for f in os.listdir(path_read) if 'reg_' in f]

    # load dti image
    img_dti = nib.load(dir_list[0])
    img_affine = img_dti.get_affine()
    dti = img_dti.get_data()
    dti_shape = dti.shape
    DTI_tensors = np.zeros((dti_shape[0], dti_shape[1], dti_shape[2], 6))

    for i, path_file in enumerate(dir_list):
        img_buffer = nib.load(path_file)
        data_buffer = img_buffer.get_data()
        DTI_tensors[:, :, :, i] = data_buffer

    array_img = nib.Nifti1Image(DTI_tensors, img_affine)
    array_img.to_filename(tensor_path)


def nii2mha_dti(data_filepath, output_filepath):
    image_type = itk.Image[itk.F, 4]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()
    reader.SetFileName(data_filepath)
    reader.Update()
    out = reader.GetOutput()
    T1 = itk_py_converter.GetArrayFromImage(out)

    # Get the header information needs to be 3d
    def get_header(data_filepath):

        image_type = itk.Image[itk.F, 3]
        itk_py_converter = itk.PyBuffer[image_type]
        reader = itk.ImageFileReader[image_type].New()
        reader.SetFileName(data_filepath)
        reader.Update()
        out = reader.GetOutput()
        return (out.GetSpacing(), out.GetOrigin())
    header_info = get_header(data_filepath)

    tensor_array = np.zeros((T1.shape[0] * T1.shape[1], T1.shape[2], T1.shape[3]), dtype=np.float32)
    for id, tensor in enumerate(T1):
        tensor_array[id * T1.shape[1]:(id + 1) * T1.shape[1], :, :] = tensor
    tensor_array = tensor_array[:, ::-1, ::-1]
    image_type_write = itk.Image[itk.F, 3]
    itk_py_converter_write = itk.PyBuffer[image_type_write]
    writer = itk.ImageFileWriter[image_type_write].New()
    writer.SetFileName(output_filepath)
    itk_image = itk_py_converter_write.GetImageFromArray(tensor_array.tolist())
    itk_image.SetSpacing(header_info[0])
    itk_image.SetOrigin(0)

    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()
    del itk_image
    del writer
    del reader
