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
STUDY_PATH = '/mnt/e/WB-MotionQuartet/derivatives'
SUB = ['sub-07']
TASK = ['amb']

for su in SUB:
    print('Working on {}'.format(su))

    # // Load VMR
    FILE_VMR = glob(os.path.join(STUDY_PATH, su, 'anat', '00_preps_MNI', '*_acq-mp2rage_UNI_denoised_IIHC_ISOpt6.vmr'))[0]
    header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)

    for ta in TASK:
        # VTC_list = glob(os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '{}_task-{}_acq-2depimb4_*_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native.vtc'.format(su, ta)))
        VTC_list = glob(os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '{}_task-amb_acq-2depimb4_run-03_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native.vtc'.format(su)))
        for VTC_file in VTC_list:

            # Load VTC
            header, tdata = bvbabel.vtc.read_vtc(VTC_file, rearrange_data_axes=False)
            print('Dimension of VTC {}'.format(np.shape(tdata)))

            # VTC -> NIFTI entire time series
            tdata = np.transpose(tdata, [0, 2, 1, 3])
            tdata = tdata[::-1, ::-1, ::-1, :]
            tdata.astype(np.float32)
            print('Dimension of NIFTI at 1.8 {}'.format(np.shape(tdata)))
            basename = VTC_file.split(os.extsep, 1)[0]
            outname = "{}_bvbabel_resx1_float32.nii.gz".format(basename)
            temp = np.eye(4)
            temp[0, 0] *= 3.0
            temp[1, 1] *= 3.0
            temp[2, 2] *= 3.0
            temp[3, 3] *= 3.0

            img = nb.Nifti1Image(tdata, affine=temp)
            img.header["pixdim"][0] = 3  # mm
            img.header["pixdim"][1] = 3  # mm
            img.header["pixdim"][2] = 3  # mm
            nb.save(img, outname)
            print("Finished.")
