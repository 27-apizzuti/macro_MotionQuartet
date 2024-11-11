"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
TASKS = ['rest', 'phy', 'amb']
LAG = 3

for task in TASKS:

    # Input file
    SEED_CORR1 = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_-{}_CORR_brainmask.nii.gz'.format(task, LAG))
    SEED_CORR1_THR = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_-{}_PVAL_THR_brainmask.nii.gz'.format(task, LAG))

    SEED_CORR2 = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_{}_CORR_brainmask.nii.gz'.format(task, LAG))
    SEED_CORR2_THR = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_{}_PVAL_THR_brainmask.nii.gz'.format(task, LAG))

    REF_VMP = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_amb_task_conjunction_models_thre_4.vmp')

    # LAG -2 // Pushing back the seed time series means that this ROI is FOLLOWING
    nii =  nb.load(SEED_CORR1)
    seed_corr1 = np.asarray(nii.dataobj)
    idx_pos1 = seed_corr1 > 0

    nii =  nb.load(SEED_CORR1_THR)
    seed_corr1_thr = np.asarray(nii.dataobj)
    idx1 =  (seed_corr1_thr == 1)

    # LAG 2 // // Pushing forward the seed time series means that this ROI is DRIVING
    nii =  nb.load(SEED_CORR2)
    seed_corr2 = np.asarray(nii.dataobj)
    idx_pos2 = seed_corr2 > 0

    nii =  nb.load(SEED_CORR2_THR)
    seed_corr2_thr = np.asarray(nii.dataobj)
    idx2 = (seed_corr2_thr == 1)

    # Only voxels that have significant correlation are considered
    idx_combined = (idx1 + idx2) * idx_pos1 * idx_pos2
    # idx_combined = idx_pos1 * idx_pos2

    # Get difference
    diff = seed_corr2 - seed_corr1

    # Remove voxels for which the difference comes from non-significant pvalue
    seed_corr_consistency_diff = np.zeros(np.shape(seed_corr2_thr))
    seed_corr_consistency_diff[idx_combined] = diff[idx_combined]
    seed_corr_consistency_diff[seed_corr_consistency_diff > 0 ] = 1
    seed_corr_consistency_diff[seed_corr_consistency_diff < 0 ] = -1

    # Sum positive
    idx_pos = (seed_corr_consistency_diff == 1)
    driving = np.sum(idx_pos, axis=-1)

    # Sum negative
    idx_neg = seed_corr_consistency_diff == -1
    following = np.sum(idx_neg, axis=-1)


    # Read VMP
    header, data = bvbabel.vmp.read_vmp(REF_VMP)
    new_vmp_data = np.concatenate((data[..., None], driving[..., None], following[..., None]), axis=3)
    print(np.shape(new_vmp_data))

    # VMP preparation
    new_vmp_header = copy(header)
    new_vmp_header['NrOfSubMaps'] += 2

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][1]["MapName"] = 'Driving - consistency'.format(task)
    new_vmp_header["Map"][1]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 1], dtype=np.int32)
    new_vmp_header["Map"][1]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][1]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][1]["UpperThreshold"] = 9
    new_vmp_header["Map"][1]["MapThreshold"] = 1
    new_vmp_header["Map"][1]['LUTFileName']= '<default>'

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][2]["MapName"] = 'Following - consistency'.format(task)
    new_vmp_header["Map"][2]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 2], dtype=np.int32)
    new_vmp_header["Map"][2]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][2]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][2]["UpperThreshold"] = 9
    new_vmp_header["Map"][2]["MapThreshold"] = 1
    new_vmp_header["Map"][2]['LUTFileName']= '<default>'

    # Save VMP
    basename = REF_VMP.split(os.extsep, 1)[0]
    OUTNAME = "{}_{}_GROUPSTAT_follow_drive_consistency_LAG{}_SEPARATEs.vmp".format(basename, task, LAG)
    bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
