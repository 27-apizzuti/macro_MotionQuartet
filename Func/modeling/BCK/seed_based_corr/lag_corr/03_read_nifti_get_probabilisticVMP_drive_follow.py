"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
TASK = 'rest'
LAG = 2

SEED_CORR = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_0_CORR.nii.gz'.format(TASK))
SEED_CORR1 = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_-{}_CORR.nii.gz'.format(TASK, LAG))
SEED_CORR2 = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_{}_CORR.nii.gz'.format(TASK, LAG))
REF_VMP = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_conjunction_model2_thre_4_SEED_MT_plus.vmp')
THR = 0.2

# LAG 0 // We use LAG 0 to threshold our map to begin with
nii =  nb.load(SEED_CORR)
seed_corr = np.asarray(nii.dataobj)
avg = np.mean(seed_corr, axis=-1)

# Threshold averaged correlatio map // Across subjects
avg_thr = copy(avg)
idx = avg_thr < THR    # --> we write zero
avg_thr[idx] = 0
avg_thr[avg > 0] = 1

# LAG -2 // Pushing back the seed time series means that this ROI is DRIVING
nii =  nb.load(SEED_CORR1)
seed_corr1 = np.asarray(nii.dataobj)
# seed_corr1[seed_corr1 < 0] = 0
# seed_corr1[seed_corr1 < 0.1] = 0


# LAG 2 // // Pushing forward the seed time series means that this ROI is FOLLOWING
nii =  nb.load(SEED_CORR2)
seed_corr2 = np.asarray(nii.dataobj)
# seed_corr2[seed_corr2 < 0] = 0
# seed_corr2[seed_corr2 < 0.1] = 0

idx_combined = (seed_corr1 > 0.1) * (seed_corr2 > 0.1)
# Get difference
seed_corr_consistency_diff = seed_corr1 - seed_corr2

seed_corr_consistency_diff[seed_corr_consistency_diff > 0] = 1
seed_corr_consistency_diff[seed_corr_consistency_diff < 0] = -1
seed_corr_consistency_diff[~idx_combined] = 0

seed_corr_consistency_diff = np.sum(seed_corr_consistency_diff, axis=-1)
seed_corr_consistency_diff[idx] = 0

# Read VMP
header, data = bvbabel.vmp.read_vmp(REF_VMP)
new_vmp_data = np.concatenate((data, avg_thr[..., None], avg[..., None], seed_corr_consistency_diff[..., None]), axis=3)
print(np.shape(new_vmp_data))

# VMP preparation
new_vmp_header = copy(header)
new_vmp_header['NrOfSubMaps'] += 3

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][3]["MapName"] = '{} Group mask'.format(TASK)
new_vmp_header["Map"][3]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 3], dtype=np.int32)
new_vmp_header["Map"][3]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][3]["ShowPosNegValues"] = 0
new_vmp_header["Map"][3]["UpperThreshold"] = 1
new_vmp_header["Map"][3]["MapThreshold"] = 0
new_vmp_header["Map"][3]['LUTFileName']= '<default>'

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][4]["MapName"] = '{} Average corr seed 0'.format(TASK)
new_vmp_header["Map"][4]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 4], dtype=np.int32)
new_vmp_header["Map"][4]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][4]["ShowPosNegValues"] = 0
new_vmp_header["Map"][4]["UpperThreshold"] = 1
new_vmp_header["Map"][4]["MapThreshold"] = 0
new_vmp_header["Map"][4]['LUTFileName']= '<default>'

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][5]["MapName"] = '{} Drive minus follow - consistency'.format(TASK)
new_vmp_header["Map"][5]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 5], dtype=np.int32)
new_vmp_header["Map"][5]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][5]["ShowPosNegValues"] = 2
new_vmp_header["Map"][5]["UpperThreshold"] = 9
new_vmp_header["Map"][5]["MapThreshold"] = 1
new_vmp_header["Map"][5]['LUTFileName']= '<default>'

# Save VMP
basename = REF_VMP.split(os.extsep, 1)[0]
OUTNAME = "{}_{}_GROUPSTAT_follow_drive_consistency_LAG{}_OLD_METHOD.vmp".format(basename, TASK, LAG)
bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
