"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

SEED_CORR = os.path.join(STUDY_PATH, 'GroupStat', 'seed_based_correlation', 'AllSbj_task-amb_MNI_seed_corr_avg.nii.gz')
SEED_CORR1 = os.path.join(STUDY_PATH, 'GroupStat', 'seed_based_correlation', 'AllSbj_task-amb_MNI_seed_corr_avg_-2.nii.gz')
SEED_CORR2 = os.path.join(STUDY_PATH, 'GroupStat', 'seed_based_correlation', 'AllSbj_task-amb_MNI_seed_corr_avg_2.nii.gz')
REF_VMP = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_conjunction_model2_thre_4_SEED_MT_plus.vmp')
THR = 0.2

# LAG 0
nii =  nb.load(SEED_CORR)
seed_corr = np.asarray(nii.dataobj)
idx = seed_corr < THR    # --> we write zero


# LAG -2
nii =  nb.load(SEED_CORR1)
seed_corr1 = np.asarray(nii.dataobj)
# LAG 2
nii =  nb.load(SEED_CORR2)
seed_corr2 = np.asarray(nii.dataobj)

# Get difference
seed_corr_consistency_diff = seed_corr1 - seed_corr2
seed_corr_consistency_diff[idx] = 0
seed_corr_consistency_diff[seed_corr_consistency_diff > 0] = 1
seed_corr_consistency_diff[seed_corr_consistency_diff < 0] = -1
seed_corr_consistency_diff = np.sum(seed_corr_consistency_diff, axis=-1)


# Read VMP
header, data = bvbabel.vmp.read_vmp(REF_VMP)
new_vmp_data = np.concatenate((data, seed_corr_consistency_diff[..., None]), axis=3)
print(np.shape(new_vmp_data))

# VMP preparation
new_vmp_header = copy(header)
new_vmp_header['NrOfSubMaps'] += 1

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][3]["MapName"] = 'Drive minus follow - consistency'
new_vmp_header["Map"][3]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 3], dtype=np.int32)
new_vmp_header["Map"][3]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][3]["ShowPosNegValues"] = 1
new_vmp_header["Map"][3]["UpperThreshold"] = 9
new_vmp_header["Map"][3]["MapThreshold"] = 1
new_vmp_header["Map"][3]['LUTFileName']= '<default>'

# Save VMP
basename = REF_VMP.split(os.extsep, 1)[0]
OUTNAME = "{}_GROUPSTAT_follow_drive_consistency.vmp".format(basename)
bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
