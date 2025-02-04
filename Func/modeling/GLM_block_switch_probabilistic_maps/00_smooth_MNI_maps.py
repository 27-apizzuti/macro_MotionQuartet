''' Smooth MNI vmps for group analyis (2vox and 3vox FWHM) '''


import os, copy
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from scipy import ndimage
import subprocess
from nilearn.image import smooth_img
import glob

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ["sub-01"]
SMOOTHING = 2 # smoothing FWHM
# =============================================================================

for su in SUBJ:

    print('Working on subject: ', su)

    PATH_IN = os.path.join(STUDY_PATH, su, 'func', 'GLM_model1','MultiRuns')

    vmps = sorted(glob.glob(f'{PATH_IN}/*sub-01_amb_model1.vmp'))

    for file in vmps:

        hdr, data = bvbabel.vmp.read_vmp(file)

        nii = nb.Nifti1Image(data, np.eye(4))

        # smooth 2 voxels (the functions requests FWHM in mm, but the nifti has artificial resolution of 1mm)
        nii_smoothed = smooth_img(nii, 2)

        smoothed_data = nii_smoothed.get_fdata()

        outname = file[:-4] + f'_smoothedFWHM{SMOOTHING}vox.vmp'
        bvbabel.vmp.write_vmp(outname, hdr, smoothed_data)
