"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from glob import glob

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
NII_FOLDER = '/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR'
REF_NIFTI = '/mnt/e/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel.nii.gz'

FILES = glob(os.path.join(NII_FOLDER, 'Glasser_MNI_bilateral_NATIVE_MANUAL_vmp_bvbabel.nii.gz'))
for nii_file in FILES:

    nii =  nb.load(nii_file)
    data = np.asarray(nii.dataobj)
    nii_rf =  nb.load(REF_NIFTI)

    # Save all time course for topup
    print('Save')
    img = nb.Nifti1Image(data, affine=nii_rf.affine, header=nii_rf.header)
    nb.save(img, nii_file)

# # Brainmask
# nii_rf =  nb.load(REF_NIFTI)
# data = np.asarray(nii_rf.dataobj)
# data[data > 0] = 1
# img = nb.Nifti1Image(data, affine=nii_rf.affine, header=nii_rf.header)
# nb.save(img, '/mnt/e/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel_brainmask.nii.gz')
