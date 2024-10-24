"""Create seed within the MT+ complex."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy
from scipy.stats import pearsonr
import time

MODEL = 'model2'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
RUNS = [1, 2, 3, 4]
LAG = -2      # seconds
STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
VMP_REF = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/AllSbj_conjunction_{}_thre_4_SEED_MT_plus.vmp".format(MODEL)

# Load nifti to take the header
NIFTI_REF = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/AllSbj_conjunction_model2_thre_4_bvbabel.nii.gz"
nii =  nb.load(NIFTI_REF)

# Load VMP
header, data = bvbabel.vmp.read_vmp(VMP_REF)
temp = data[..., -1]
idx = (temp == 1)
print('Number of voxels considered as SEED: {}'.format(np.sum(idx)))

for su in SUBJ:
    PATH_VTC = os.path.join(STUDY_PATH, su, 'func', 'VTC_MNI')
    PATH_OUT = os.path.join(STUDY_PATH, su, 'func', 'SEED_CORR')
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)
    for run in RUNS:
        print('Working on {} run {}'.format(su, run))
        VTC_FILE = '{}_task-amb_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc'.format(su, run)
        VTC = os.path.join(PATH_VTC, VTC_FILE)

        # // Read VTC
        header_vtc, data_vtc =  bvbabel.vtc.read_vtc(VTC)
        dims_VTC = np.shape(data_vtc)

        # Prepare SEED tc
        seed_tc = data_vtc[idx, :]
        seed_avg_tc = np.mean(seed_tc, 0)

        # Circolar shift (positive go forward)
        seed_avg_tc = np.roll(seed_avg_tc, LAG)
        # Normalize the seed time series and voxel time series
        seed_mean = np.mean(seed_avg_tc)
        seed_std = np.std(seed_avg_tc)
        # Subtract the mean and divide by the standard deviation (z-score normalization)
        seed_z  = (seed_avg_tc - seed_mean) / seed_std
        # Reshape the 4D matrix to a 2D matrix
        voxels_time_series = data_vtc.reshape(-1, dims_VTC[-1])
        # Normalize each voxel's time series across the 600 time points
        voxel_mean = np.mean(voxels_time_series, axis=1, keepdims=True)
        voxel_std = np.std(voxels_time_series, axis=1, keepdims=True)
        # Z-score normalization for voxel time series
        voxels_z = (voxels_time_series - voxel_mean) / voxel_std

        # Initialize an array to store correlation values
        correlation_map = np.zeros(voxels_time_series.shape[0])

        # Start the timer
        start_time = time.time()
        # Compute the Pearson correlation in a vectorized way (dot product of normalized values)
        correlation_map = np.dot(voxels_z, seed_z) / dims_VTC[-1]  # Correlation across 600 time points

        # Reshape the correlation map back to the original 3D shape (10x10x10)
        correlation_map_3d = correlation_map.reshape(dims_VTC[0], dims_VTC[1], dims_VTC[2])
        end_time = time.time() # End the timer and calculate the total time taken
        print(f"Time taken: {end_time - start_time} seconds")

        # Save group voxels
        basename = VTC_FILE.split(os.extsep, 1)[0]
        outname = os.path.join(PATH_OUT, "{}_seed_corr_{}.nii.gz".format(basename, LAG))
        img = nb.Nifti1Image(correlation_map_3d, header=nii.header, affine=nii.affine)
        nb.save(img, outname)

print("Finished.")
