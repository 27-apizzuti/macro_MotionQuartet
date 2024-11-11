"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
LAG = 0
SEED_CORR = os.path.join(STUDY_PATH, 'GroupStat', 'seed_based_correlation', 'AllSbj_task-amb_MNI_seed_corr_avg_{}.nii.gz'.format(LAG))
REF_VMP = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_conjunction_model2_thre_4_SEED_MT_plus.vmp')
THR = 0.2

# Read nifti apply threshold
nii =  nb.load(SEED_CORR)
seed_corr = np.asarray(nii.dataobj)

# Get average
seed_corr_avg = np.mean(seed_corr, axis=-1)
print(np.shape(seed_corr_avg))
idx = seed_corr_avg < THR
seed_corr_avg[idx] = 0

# Get consistency
seed_corr[seed_corr < THR] = 0
seed_corr[seed_corr > THR] = 1
seed_corr_consistency = np.sum(seed_corr, axis=-1)
seed_corr_consistency[idx] = 0

# Read VMP
header, data = bvbabel.vmp.read_vmp(REF_VMP)
print(np.shape(data))
new_vmp_data = np.concatenate((data, seed_corr_avg[..., None], seed_corr_consistency[..., None]), axis=3)
print(np.shape(new_vmp_data))

# VMP preparation
new_vmp_header = copy(header)
new_vmp_header['NrOfSubMaps'] += 2
new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][3]["MapName"] = 'Group average'
new_vmp_header["Map"][3]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 3], dtype=np.int32)
new_vmp_header["Map"][3]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][3]["ShowPosNegValues"] = 1
new_vmp_header["Map"][3]["UpperThreshold"] = 0.7
new_vmp_header["Map"][3]["MapThreshold"] = THR
new_vmp_header["Map"][3]['LUTFileName']= '<default>'

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][4]["MapName"] = 'Group consistency'
new_vmp_header["Map"][4]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 4], dtype=np.int32)
new_vmp_header["Map"][4]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][4]["ShowPosNegValues"] = 1
new_vmp_header["Map"][4]["UpperThreshold"] = 9
new_vmp_header["Map"][4]["MapThreshold"] = 1
new_vmp_header["Map"][4]['LUTFileName']= '<default>'

# Save VMP
basename = REF_VMP.split(os.extsep, 1)[0]
OUTNAME = "{}_GROUPSTAT_{}.vmp".format(basename, LAG)
bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
