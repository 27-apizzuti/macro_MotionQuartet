"""Create seed within the MT+ complex."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy
from scipy.stats import t as t_dist
import time

MODEL = 'model2'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
LAGS = [-3, -2, -1, 0, 1, 2, 3]      # seconds
TASKS = ['amb', 'phy', 'rest']

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
VMP_REF = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR/AllSbj_conjunction_{}_thre_4_SEED_MT_plus.vmp".format(MODEL)

# Load nifti to take the header
NIFTI_REF = "/mnt/e/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel_brainmask.nii.gz"
nii =  nb.load(NIFTI_REF)

# Load VMP
header, data = bvbabel.vmp.read_vmp(VMP_REF)
temp = data[..., -1]
idx = (temp == 1)
print('Number of voxels considered as SEED: {}'.format(np.sum(idx)))

for TASK in TASKS:
    if TASK == 'rest':
        RUNS = [1]
    if TASK == 'phy':
        RUNS = [1, 2]
    if TASK == 'amb':
        RUNS = [1, 2, 3, 4]

    for lag in LAGS:
        print('Starting with LAG: {}'.format(lag))

        for su in SUBJ:
            PATH_VTC = os.path.join(STUDY_PATH, su, 'func', 'VTC_MNI')
            PATH_OUT = os.path.join(STUDY_PATH, su, 'func', 'SEED_CORR')

            if not os.path.exists(PATH_OUT):
                os.mkdir(PATH_OUT)

            for run in RUNS:
                print('Working on {} run {}'.format(su, run))
                VTC_FILE = '{}_task-{}_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc'.format(su, TASK, run)
                VTC = os.path.join(PATH_VTC, VTC_FILE)

                # // Read VTC
                header_vtc, data_vtc =  bvbabel.vtc.read_vtc(VTC)
                dims_VTC = np.shape(data_vtc)

                # Prepare SEED tc
                seed_tc = data_vtc[idx, :]
                seed_avg_tc = np.mean(seed_tc, 0)

                if lag == 0:
                    seed_avg_tc = seed_avg_tc
                else:
                    # Circolar shift (positive go forward)
                    seed_avg_tc = np.roll(seed_avg_tc, lag)

                # Normalize (z-score) the seed time series and voxel time series
                seed_mean = np.mean(seed_avg_tc)
                seed_std = np.std(seed_avg_tc)
                seed_z  = (seed_avg_tc - seed_mean) / seed_std

                # Reshape the 4D matrix to a 2D matrix
                voxels_time_series = data_vtc.reshape(-1, dims_VTC[-1])
                voxel_mean = np.mean(voxels_time_series, axis=1, keepdims=True)
                voxel_std = np.std(voxels_time_series, axis=1, keepdims=True)
                voxels_z = (voxels_time_series - voxel_mean) / voxel_std

                # Initialize an array to store correlation values
                correlation_map = np.zeros(voxels_time_series.shape[0])

                # Start the timer
                start_time = time.time()
                correlation_map = np.dot(voxels_z, seed_z) / dims_VTC[-1]  # Correlation across 600 time points

                # Calculate p-values from correlation coefficients
                n = dims_VTC[-1]  # Number of time points
                t_stats = correlation_map * np.sqrt((n - 2) / (1 - correlation_map ** 2))  # t-statistics
                p_value_map = 2 * t_dist.sf(np.abs(t_stats), df=n - 2)                     # Two-tailed p-values

                # Reshape the correlation and p-value maps back to the original 3D shape (10x10x10)
                correlation_map_3d = correlation_map.reshape(dims_VTC[0], dims_VTC[1], dims_VTC[2])
                p_value_map_3d = p_value_map.reshape(dims_VTC[0], dims_VTC[1], dims_VTC[2])
                p_value_map_3d = p_value_map_3d.astype(np.float32)

                # Reshape the correlation map back to the original 3D shape (10x10x10)
                end_time = time.time() # End the timer and calculate the total time taken
                print(f"Time taken: {end_time - start_time} seconds")

                # Save correlation map
                basename = VTC_FILE.split(os.extsep, 1)[0]
                outname = os.path.join(PATH_OUT, "{}_seed_corr_{}.nii.gz".format(basename, lag))
                img = nb.Nifti1Image(correlation_map_3d, header=nii.header, affine=nii.affine)
                nb.save(img, outname)

                outname = os.path.join(PATH_OUT, "{}_seed_corr_{}_pval.nii.gz".format(basename, lag))
                img = nb.Nifti1Image(p_value_map_3d, header=nii.header, affine=nii.affine)
                img.header.set_data_dtype(np.float64)
                nb.save(img, outname)

print("Finished.")
