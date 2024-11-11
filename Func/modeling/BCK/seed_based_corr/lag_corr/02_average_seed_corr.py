"""Read single run seed-based correlation and average them"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
RUNS = [1, 2, 3, 4]
LAGS = [0]
TASK = 'amb'
avg_corr_sbj = np.zeros([99, 127, 90, len(SUBJ)])

for lag in LAGS:
    for itsu, su in enumerate(SUBJ):

        PATH_IN = os.path.join(STUDY_PATH, su, 'func', 'SEED_CORR', 'control')
        avg_corr = np.zeros([99, 127, 90])

        for run in RUNS:
            FILE = '{}_task-{}_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI_seed_corr_{}.nii.gz'.format(su, TASK, run, lag)

            # Load nifti
            nii =  nb.load(os.path.join(PATH_IN, FILE))
            seed_corr = np.asarray(nii.dataobj)
            avg_corr = avg_corr + seed_corr

        # Compute average
        avg_corr = avg_corr / len(RUNS)

        # Save AVG_CORR - SEED
        outname = os.path.join(PATH_IN, "{}_task-{}_MNI_seed_corr_avg_{}.nii.gz".format(su, TASK, lag))
        img = nb.Nifti1Image(avg_corr, affine=np.eye(4))
        nb.save(img, outname)

        # Put all subjects into a nifti
        avg_corr_sbj[..., itsu] = avg_corr

    # Save ALL SUBJECTS
    outname = os.path.join(PATH_IN, 'AllSbj_task-{}_MNI_seed_corr_avg_{}.nii.gz'.format(TASK, lag))
    img = nb.Nifti1Image(avg_corr_sbj, affine=np.eye(4))
    nb.save(img, outname)

print("Finished.")
