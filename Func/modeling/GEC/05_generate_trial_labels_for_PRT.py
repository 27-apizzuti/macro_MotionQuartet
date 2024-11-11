"""Uniquely label each trial in carpet protocols.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb

# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
TASK = 'phy'
MAIN_PATH = '/mnt/e/WB-MotionQuartet'
# =============================================================================

for su in SUBJ:

    PATH_IN = os.path.join(MAIN_PATH, 'derivatives', su, 'func', 'GEC')
    NII_PRT = os.path.join(PATH_IN, f"{su}_{TASK}_VOICarpet_PRT_MotFlick.nii.gz")

    # -----------------------------------------------------------------------------
    # Load nifti time course
    nii = nb.load(NII_PRT)
    data = np.asarray(nii.dataobj)

    nr_timepoints = data.shape[0]
    nr_voxels = data.shape[1]
    print(f"  Nr. timepoints {nr_timepoints}")
    print(f"  Nr. voxels {nr_voxels}")

    # One line is enough
    data = data[:, 0]

    # Find the indices where the consecutive blocks start
    block_indices = np.flatnonzero(data[:-1] != data[1:]) + 1
    block_indices = np.concatenate(([0], block_indices, [len(data)]))

    # Assign unique labels to each consecutive block
    labels = np.arange(len(block_indices) - 1)

    # Create an array with the labels for each element in the original data
    labeled_data = np.zeros_like(data)
    for i in range(len(block_indices) - 1):
        labeled_data[block_indices[i]:block_indices[i+1]] = labels[i]

    print("  Original Data:", data)
    print("  Labeled Data:", labeled_data)

    temp = np.zeros(nii.shape)
    temp += labeled_data[:, None]

    # Count number of uniques to determine duration
    uniques, counts = np.unique(temp[:, 0], return_counts=True)

    temp2 = np.copy(temp)
    for i in range(uniques.size):
        idx = temp == uniques[i]
        temp2[idx] = counts[i]

    # Save
    filename = os.path.basename(NII_PRT)
    basename, ext = filename.split(os.extsep, 1)

    outname = os.path.join(PATH_IN, f"{basename}_labels-trials.nii.gz")
    img = nb.Nifti1Image(temp, affine=nii.affine)
    nb.save(img, outname)

    outname = os.path.join(PATH_IN, f"{basename}_labels-durations.nii.gz")
    img = nb.Nifti1Image(temp2, affine=nii.affine)
    nb.save(img, outname)


print("\nFinished.")
