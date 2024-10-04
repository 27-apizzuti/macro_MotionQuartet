"""Prepare data for computing extra affine matrices for appling correctly MNI transformation"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from scipy import ndimage
import subprocess
from glob import glob

# Settings
mni_bbox = {'XStart': 108,
                'XEnd': 405,
                'YStart': 90,
                'YEnd': 471,
                'ZStart': 100,
                'ZEnd': 370}

# Load NIFTI ANAT MNI at 0.6 iso mm
ANT_MNI = "/mnt/d/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6_bvbabel.nii.gz"

# Load data and perform zeroing to reduce the dimension
data = nb.load(ANT_MNI).get_fdata()
mask = np.zeros(data.shape)

mask[mni_bbox["XStart"]-1:mni_bbox["XEnd"]-1,
	mni_bbox["YStart"]-1:mni_bbox["YEnd"]-1,
	 mni_bbox["ZStart"]-1:mni_bbox["ZEnd"]-1] = 1

mask = mask[::-1,::-1,::-1]
data = data * mask

new_data = data[512 - mni_bbox["XEnd"] : 512 - mni_bbox["XStart"],
		   512 - mni_bbox["YEnd"] : 512 - mni_bbox["YStart"] ,
		   512 - mni_bbox["ZEnd"] : 512 - mni_bbox["ZStart"]
		   ]
# Reduce shape
print('Save NII as nifti at 1pt8 res')
ANT_MNI_DOWN = "/mnt/d/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel.nii.gz"
reduced_data = ndimage.zoom(new_data, (1/3, 1/3, 1/3), order=0, output=np.float32)
temp = np.eye(4)
temp[0, 0] *= 3.0
temp[1, 1] *= 3.0
temp[2, 2] *= 3.0
temp[3, 3] *= 3.0
nii = nb.Nifti1Image(reduced_data.astype(float), affine=temp)
nii.header["pixdim"][1] = 3  # mm
nii.header["pixdim"][2] = 3  # mm
nii.header["pixdim"][3] = 3  # mm
nb.save(nii, ANT_MNI_DOWN)
