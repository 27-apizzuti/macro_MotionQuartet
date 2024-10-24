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
THR = 0.25


# LAG 0
nii =  nb.load(SEED_CORR)
seed_corr = np.asarray(nii.dataobj)
seed_corr_avg = np.median(seed_corr, axis=-1)

# LAG -2
nii =  nb.load(SEED_CORR1)
seed_corr1 = np.asarray(nii.dataobj)
seed_corr_avg1 = np.median(seed_corr1, axis=-1)

# LAG 2
nii =  nb.load(SEED_CORR2)
seed_corr2 = np.asarray(nii.dataobj)
# Get average
seed_corr_avg2 = np.median(seed_corr2, axis=-1)

seed_corr_consistency_diff = seed_corr_avg1 - seed_corr_avg2

# Read VMP
header, data = bvbabel.vmp.read_vmp(REF_VMP)
new_vmp_data = np.concatenate((data, seed_corr_avg[..., None], seed_corr_avg1[..., None], seed_corr_avg2[..., None], seed_corr_consistency_diff[..., None]), axis=3)
print(np.shape(new_vmp_data))

# VMP preparation
new_vmp_header = copy(header)
new_vmp_header['NrOfSubMaps'] += 4

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][3]["MapName"] = 'LAG 0'
new_vmp_header["Map"][3]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 3], dtype=np.int32)
new_vmp_header["Map"][3]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][3]["ShowPosNegValues"] = 1
new_vmp_header["Map"][3]["UpperThreshold"] = 0.7
new_vmp_header["Map"][3]["MapThreshold"] = THR
new_vmp_header["Map"][3]['LUTFileName']= '<default>'

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][4]["MapName"] = 'LAG -2, drive'
new_vmp_header["Map"][4]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 4], dtype=np.int32)
new_vmp_header["Map"][4]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][4]["ShowPosNegValues"] = 1
new_vmp_header["Map"][4]["UpperThreshold"] = 0.7
new_vmp_header["Map"][4]["MapThreshold"] = THR
new_vmp_header["Map"][4]['LUTFileName']= '<default>'

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][5]["MapName"] = 'LAG +2, follow'
new_vmp_header["Map"][5]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 5], dtype=np.int32)
new_vmp_header["Map"][5]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][5]["ShowPosNegValues"] = 1
new_vmp_header["Map"][5]["UpperThreshold"] = 0.7
new_vmp_header["Map"][5]["MapThreshold"] = THR
new_vmp_header["Map"][5]['LUTFileName']= '<default>'

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][6]["MapName"] = 'Drive minus follow'
new_vmp_header["Map"][6]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 6], dtype=np.int32)
new_vmp_header["Map"][6]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][6]["ShowPosNegValues"] = 2
new_vmp_header["Map"][6]["UpperThreshold"] = 0.2
new_vmp_header["Map"][6]["MapThreshold"] = THR
new_vmp_header["Map"][6]['LUTFileName']= '<default>'

print(new_vmp_header["Map"][5]["MapName"])
# Save VMP
basename = REF_VMP.split(os.extsep, 1)[0]
OUTNAME = "{}_GROUPSTAT_follow_drive.vmp".format(basename)
bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
