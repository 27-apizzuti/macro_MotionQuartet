"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy

# Quick and dirty
REF_VMR = "/mnt/e/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr"
NIFTI = "/mnt/e/WB-MotionQuartet/derivatives/Glasser_atlas/MNI_Glasser_HCP_resliced_NN_pt6.nii.gz"

header, data = bvbabel.vmr.read_vmr(REF_VMR)
print('Converting NIFTI to VMR')

# Load nifti to convert
nii =  nb.load(NIFTI)
datanii = np.asarray(nii.dataobj)
data2 = copy(datanii)

datanii[datanii > 180] = 0
print(np.unique(datanii))
outname = "/mnt/e/WB-MotionQuartet/derivatives/Glasser_atlas/Glasser_MNI_resliced_brainvoyager_pt6_LH.vmr"
bvbabel.vmr.write_vmr(outname, header, datanii)

data2[data2 < 1000] = 0
data2 = data2 - 1000

data2[data2 < 0] = 0

print(np.unique(data2))
outname = "/mnt/e/WB-MotionQuartet/derivatives/Glasser_atlas/Glasser_MNI_resliced_brainvoyager_pt6_RH.vmr"
bvbabel.vmr.write_vmr(outname, header, data2)
