import os
import argparse
import glob
import fnmatch
import ipdb
import numpy as np
import itk
from multiprocessing import Pool
import subprocess
import ipdb
import sys

def preprocess_file(entry_filepath, mask_filepath, extension, n4itk_modalities):

    print entry_filepath
    #ipdb.set_trace()

    if "OT" not in entry_filepath:

        cmd = "ImageMath 3 {0}_trunk.{1} TruncateImageIntensity {0} 0.01 0.99 200".format(entry_filepath, extension)
        print cmd
        subprocess.call(cmd, shell=True)

        #If we do the N4ITK preprocess for that modalitie:

        for m in n4itk_modalities:
            if m in entry_filepath:

                print "Oh! doing", entry_filepath
                #if "T1" in entry_filepath:
                cmd = "N4BiasFieldCorrection -d 3 -i {0}_trunk.{2} -x {1} -o {0}_N4ITK_temp1.{2} -b [200] -s 2 -c[50x50x50x10,0]".format(entry_filepath, mask_filepath, extension)
                subprocess.call(cmd, shell=True)

                cmd = "ImageMath 3 {0}_N4ITK_temp2.{2} m {1} {0}_N4ITK_temp1.{2}".format(entry_filepath, mask_filepath, extension)
                subprocess.call(cmd, shell=True)

                cmd = "rm {0}_N4ITK_temp1.{1}".format(entry_filepath, extension)
                subprocess.call(cmd, shell=True)

                cmd = "ImageMath 3 {0}_N4ITK.{2} m {1} {0}_N4ITK_temp2.{2}".format(entry_filepath, mask_filepath, extension)
                subprocess.call(cmd, shell=True)

                cmd = "rm {0}_N4ITK_temp2.{1}".format(entry_filepath, extension)
                subprocess.call(cmd, shell=True)
                return


def save_file_mask (entry_filepath, output_filepath):
    image_type = itk.Image[itk.SS, 3]
    itk_py_converter = itk.PyBuffer[image_type]
    reader = itk.ImageFileReader[image_type].New()
    reader.SetFileName(entry_filepath)
    reader.Update()
    out = reader.GetOutput()
    print 'get content'
    content = itk_py_converter.GetArrayFromImage(out)
    content = np.array(content, dtype = np.short)
    print 'get mask'
    mask = (content != 0)
    print "mask :", mask.sum(),"on",mask.size,"pixels."
    writer = itk.ImageFileWriter[image_type].New()
    writer.SetFileName(output_filepath)
    itk_image = itk_py_converter.GetImageFromArray(mask.tolist() )
    itk_image.SetSpacing(out.GetSpacing())
    itk_image.SetOrigin(out.GetOrigin())
    writer.SetInput(itk_image.GetPointer())
    writer.UseCompressionOn()
    writer.Update()

def get_all_path(root, extension):

    matches = []
    for root1, dirnames, filenames in os.walk(root):
        for filename in fnmatch.filter(filenames, "*.{}".format(extension)):
            matches.append(os.path.join(root1, filename))

    return matches

#ii = 0
def process_file((path, extension, n4itk_modalities)):

    #print "doing", path
    mask_name = path + "mask.{}".format(extension)
#    if not os.path.exists(mask_name) and "OT" not in mask_name and "mask" not in mask_name and "N4ITK" not in mask_name and "trunk" not in mask_name:
    if not os.path.exists(mask_name) and "OT" not in mask_name and "mask" not in path and "N4ITK" not in path and "trunk" not in path:

        print "{} not done.".format(path)
        save_file_mask(path, mask_name)
        preprocess_file(path, mask_name, extension, n4itk_modalities)


def preprocess_all(paths, nb_cpu, extension, n4itk_modalities):



    #for p in paths:
    #    #print p
    #    process_file(p)
    #print ii
    #f(paths[0])

    #ipdb.set_trace()
    #process_file((paths[0], extension, n4itk_modalities))
    #process_file((paths[1], extension, n4itk_modalities))
    #process_file((paths[2], extension, n4itk_modalities))
    #process_file((paths[3], extension, n4itk_modalities))
    #The preprocess
    p = Pool(nb_cpu)
    p.map(process_file, zip(paths, [extension] * len(paths), [n4itk_modalities] * len(paths)))

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Trains a model')

    parser.add_argument("--data-path", type=str, default='/media/dutf1902/DATA/brats/BRATS2014_training',
                        help='The folder contening the data to pre process.')

    parser.add_argument("--extension", type=str, default='mha',
                        help='The extention of the file (mha, nii, ...).')

    parser.add_argument("--nb-cpu", type=int, default=6,
                        help='The number of CPU to use for the preprocessing.')

    parser.add_argument("--n4itk-modalities", type=str, nargs='+', default=['T1', 'T1c'],
                        help='The modalities on which we want to do the N4ITK preprocessing')


    args = parser.parse_args()

    data_path = args.data_path
    extension = args.extension
    extension = args.extension
    nb_cpu = args.nb_cpu
    n4itk_modalities = args.n4itk_modalities


    if not os.path.exists(data_path):
        print "The folder '{}' does not exist!".format(data_path)
        sys.exit(1)

    #Getting all the file to preprocess
    matches = get_all_path(data_path, extension)

    #Preprocess them all!
    preprocess_all(matches, nb_cpu, extension, n4itk_modalities)