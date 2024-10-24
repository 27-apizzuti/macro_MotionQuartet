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

VMP_REF = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/AllSbj_conjunction_{}_thre_4_SEED_MT_plus.vmp".format(MODEL)
VTC = "/mnt/e/WB-MotionQuartet/derivatives/sub-01/func/VTC_MNI/sub-01_task-amb_run-01_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc"

# =============================================================================
# Load VMP
header, data = bvbabel.vmp.read_vmp(VMP_REF)
temp = data[..., -1]
idx = (temp == 1)
print('Number of voxels considered as SEED: {}'.format(np.sum(idx)))
header_vtc, data_vtc =  bvbabel.vtc.read_vtc(VTC)
dims_VTC = np.shape(data_vtc)
tc = data_vtc[idx, :]

seed_avg_tc = np.mean(tc, 0)

# Compute whole brain correlation map
# Reshape the 4D matrix to a 2D matrix (1000 voxels, 600 time points)
voxels_time_series = data_vtc.reshape(-1, dims_VTC[-1])

print('Total number of time series: {}'.format(np.shape(voxels_time_series)[0]))

# Initialize an array to store correlation values
correlation_map = np.zeros(voxels_time_series.shape[0])

# Start the timer
start_time = time.time()

# Compute the Pearson correlation for each voxel's time series with the seed time series
for i in range(voxels_time_series.shape[0]):
    # print(i)
    correlation_map[i], _ = pearsonr(seed_avg_tc, voxels_time_series[i])

# Reshape the correlation map back to the original 3D shape (10x10x10)
correlation_map_3d = correlation_map.reshape(dims_VTC[0], dims_VTC[1], dims_VTC[2])

# End the timer and calculate the total time taken
end_time = time.time() # End the timer and calculate the total time taken

print(f"Time taken: {end_time - start_time} seconds")

# Save group voxels
outname = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/test1_slow.nii.gz"
img = nb.Nifti1Image(correlation_map_3d, affine=np.eye(4))
nb.save(img, outname)

# Alternative computation
# Start the timer
start_time = time.time()
# Normalize the seed time series and voxel time series
seed_mean = np.mean(seed_avg_tc)
seed_std = np.std(seed_avg_tc)

# Subtract the mean and divide by the standard deviation (z-score normalization)
seed_z  = (seed_avg_tc - seed_mean) / seed_std

# Normalize each voxel's time series across the 600 time points
voxel_mean = np.mean(voxels_time_series, axis=1, keepdims=True)
voxel_std = np.std(voxels_time_series, axis=1, keepdims=True)

# Z-score normalization for voxel time series
voxels_z = (voxels_time_series - voxel_mean) / voxel_std

# Compute the Pearson correlation in a vectorized way (dot product of normalized values)
correlation_map = np.dot(voxels_z, seed_z) / dims_VTC[-1]  # Correlation across 600 time points

# Reshape the correlation map back to the original 3D shape (10x10x10)
correlation_map_3d = correlation_map.reshape(dims_VTC[0], dims_VTC[1], dims_VTC[2])
end_time = time.time() # End the timer and calculate the total time taken
print(f"Time taken: {end_time - start_time} seconds")

# Save group voxels
outname = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/test2_fast.nii.gz"
img = nb.Nifti1Image(correlation_map_3d, affine=np.eye(4))
nb.save(img, outname)

# # Save VMP
# new_vmp_data = np.concatenate((data[..., None], idx_glasser[..., None], idx_group[..., None]), axis=3)
# print(np.shape(new_vmp_data))
#
# # VMP preparation
# new_vmp_header = copy(header)
# new_vmp_header['NrOfSubMaps'] += 2
# new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
# new_vmp_header["Map"][1]["MapName"] = 'MT+ seed'
# new_vmp_header["Map"][1]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 1], dtype=np.int32)
# new_vmp_header["Map"][1]["EnableClusterSizeThreshold"] = 0
# new_vmp_header["Map"][1]["ShowPosNegValues"] = 1
# new_vmp_header["Map"][1]["UpperThreshold"] = np.max(new_vmp_data[..., 1])
# new_vmp_header["Map"][1]["MapThreshold"] = np.min(new_vmp_data[..., 1])
#
# # Save VMP
# basename = VMP_REF.split(os.extsep, 1)[0]
# OUTNAME = "{}_SEED_MT_plus.vmp".format(basename, roi)
# bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
