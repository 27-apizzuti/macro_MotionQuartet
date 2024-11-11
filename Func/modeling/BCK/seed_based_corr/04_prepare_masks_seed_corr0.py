"""Read single run seed-based correlation and average them"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
LAG = 0
TASK = 'amb'
SEED_CORR = os.path.join(STUDY_PATH, 'GroupStat', 'seed_based_correlation', 'AllSbj_task-{}_MNI_seed_corr_avg_{}.nii.gz'.format(TASK, LAG))
THR = 0.3
REF_NIFTI = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/seed_based_correlation/nifti/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel.nii.gz"

nii_ref =  nb.load(REF_NIFTI)
ref = np.asarray(nii_ref.dataobj)
idx_brainmask = (ref == 0)

# Read nifti apply threshold
nii =  nb.load(SEED_CORR)
seed_corr = np.asarray(nii.dataobj)
seed_corr[idx_brainmask, ...] = 0


# Get mask average
seed_corr_avg = np.mean(seed_corr, axis=-1)
idx = seed_corr_avg < THR
seed_corr_avg[seed_corr_avg < THR] = 0
seed_corr_avg[seed_corr_avg > THR] = 1

# Get single-subject average
seed_corr[seed_corr < THR] = 0
seed_corr[seed_corr > THR] = 1
seed_corr_consistency = np.sum(seed_corr, axis=-1)
seed_corr_consistency[idx] = 0

new_data = np.concatenate((seed_corr, seed_corr_avg[..., None], seed_corr_consistency[..., None]), axis=3)

# Save ALL SUBJECTS
outname = os.path.join(STUDY_PATH, 'GroupStat', 'seed_based_correlation', 'AllSbj_task-{}_MNI_seed_corr_avg_{}_masks.nii.gz'.format(TASK, LAG))
img = nb.Nifti1Image(new_data, affine=nii_ref.affine, header=nii_ref.header)
nb.save(img, outname)

print("Finished.")
