"""Read BrainVoyager vmr and export nifti."""


import os
import numpy as np
import nibabel as nb
import bvbabel as bv
import pprint
import subprocess
from glob import glob

STUDY_PATH = '/mnt/d/WB-MotionQuartet'
SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]
SES = [1]

new_data = np.zeros([512, 512, 512])
   
for su in SUBJ:

    print('Working on {}'.format(su))
    PATH_IN = os.path.join(STUDY_PATH, 'derivatives', su, 'anat', '00_preps_MNI', 'ANTS')
    NIFILE = glob(os.path.join(PATH_IN, '*MNIWarped.nii.gz'))[0]
    nii = nb.load(NIFILE)
    niidata = np.asarray(nii.dataobj)
    # Add subject
    print('Adding {}'.format(su))
    new_data = new_data + niidata
    print(new_data[300, 300, 300])
    print(niidata[300, 300, 300])

print('Compute the average')
new_data = new_data / len(SUBJ)
print(new_data[300, 300,300])
outname = os.path.join(STUDY_PATH, 'derivatives', 'MNI_ANTS_average.nii.gz')
img = nb.Nifti1Image(new_data, affine=nii.affine, header=nii.header)
nb.save(img, outname)

print("Finished.")


# # ------- Average VMR export nifti
# STUDY_PATH = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
# SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]

# new_data = np.zeros([256, 256, 256])
   
# for su in SUBJ:

#     print('Working on {}'.format(su))
#     PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat')
#     print(PATH_IN)
#     VMRFILE = glob(os.path.join(PATH_IN, '*ISOpt1_MNI.vmr'))[0]
    
#     header, data = bv.vmr.read_vmr(VMRFILE)
#     # Add subject
#     print('Adding {}'.format(su))
#     new_data = new_data + data

# print('Compute the average')
# new_data = new_data / len(SUBJ)

# outname = os.path.join(STUDY_PATH,  'MNI_BV_average.nii.gz')
# img = nb.Nifti1Image(new_data, affine=np.eye(4))
# nb.save(img, outname)

# print("Finished.")




