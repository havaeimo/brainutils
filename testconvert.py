from convertformats import convert_mhd_2_mha
from os import listdir
from os.path import join  # import pdb
# pdb.set_trace()
#path = '/home/local/USHERBROOKE/havm2701/data/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/temp'
#path = '/data/havm2701/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST/4SEG'
#path = '/home/local/USHERBROOKE/havm2701/data/Dropbox/PhD_MohammadH/data2/Results_Mohammad/kNN_alpha_0.08_beta_0.002/kNN_medianfilter'
# save_file_mask(join(path,'p-csf.nii.gz'),join(path,'p-csf.mha'))
# save_file_mask(join(path,'p-gray.nii.gz'),join(path,'p-gray.mha'))
# save_file_mask(join(path,'p-white.nii.gz'),join(path,'p-white.mha'))
#path = '/home/local/USHERBROOKE/havm2701/data/kNN_alpha_0.08_beta_0.002/kNN_medianfilter'
# for f in listdir(path):
#    changeheader_mha(join(path, f), '/home/local/USHERBROOKE/havm2701/data/Dropbox/PhD_MohammadH/data2/Results_Mohammad/MAXIME/000/T1/T1.mha', join(path, f))

# save_file_mask('Alighned_input/p_white.nii','Alighned_input/p_white.mha')
# save_file_mask('Alighned_input/p_gray.nii','Alighned_input/p_gray.mha')
# save_file_mask('Alighned_input/p_csf.nii','Alighned_input/p_csf.mha')

# save_file_mask('Alighned_input/p_vessel.mha','Alighned_input/p_vessel2.mha')
#path = '/data/havm2701/Synthetic_tumor_project/Synthetic_tumor/PPMI/Subject_3112_2011-06-27_243563_243565/TEST'
# save_dti(join(path,'aligned_tensors.nii.gz'),join(path,'tensors.mha'))
#path = '/data/havm2701/Data/Maxime_3modality_dataset/nii_files'
# for f in listdir(path):
#    nii2mha_int(join(path, f), join(path, f.replace('.nii.gz', '.mha')))
path = '/home/local/USHERBROOKE/havm2701/data/Data/GSP1RMCPRFRER_FR_DVD'
convert_mhd_2_mha(join(path, 'liver-orig001.mhd'), join(path, 'liver-orig001.mha'))
