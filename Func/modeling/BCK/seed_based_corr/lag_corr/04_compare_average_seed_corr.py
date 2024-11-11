"""Read single run seed-based correlation and average them"""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy

PATH_IN = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/seed_based_correlation"
LAGS = [-2, -1, 1, 2]
TASK = 'amb'

# Load the first file to initialize the max data and indices array
nii = nb.load(os.path.join(PATH_IN, 'AllSbj_task-{}_MNI_seed_corr_avg_0.nii.gz'.format(TASK)))
max_data = np.asarray(nii.dataobj)
max_data = np.abs(max_data)
max_indices = np.zeros(max_data.shape, dtype=np.int32)

for i, lag in enumerate(LAGS):
    FILE = 'AllSbj_task-{}_MNI_seed_corr_avg_{}.nii.gz'.format(TASK, lag)

    # Load nifti
    nii =  nb.load(os.path.join(PATH_IN, FILE))
    current_data = np.asarray(nii.dataobj)
    current_data = np.abs(current_data)

    # Create a boolean mask where the current data is greater than the max data
    mask = current_data > (max_data + 0.1)

    # Update max_data and max_indices where the current matrix has higher values
    max_data[mask] = current_data[mask]
    max_indices[mask] = lag  # Store the index of the matrix with the max value

    print(np.unique(max_indices))

# Save ALL SUBJECTS
outname = os.path.join(PATH_IN, 'AllSbj_task-{}_MNI_seed_corr_avg_compare_lags.nii.gz'.format(TASK))
img = nb.Nifti1Image(max_indices, affine=nii.affine, header=nii.header)
nb.save(img, outname)

print("Finished.")
