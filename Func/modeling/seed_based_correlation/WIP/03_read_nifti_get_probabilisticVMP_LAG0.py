"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
TASKS = ['phy', 'rest', 'amb']
LAG = 0

for task in TASKS:

    # Input file
    SEED_CORR = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_0_CORR_brainmask.nii.gz'.format(task, LAG))
    SEED_CORR_THR = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_task-{}_MNI_seed_corr_avg_0_PVAL_THR_brainmask.nii.gz'.format(task, LAG))

    REF_VMP = os.path.join(STUDY_PATH, 'GroupStat', 'SEED_CORR', 'AllSbj_amb_task_conjunction_models_thre_4.vmp')

    # LAG0
    nii =  nb.load(SEED_CORR)
    seed_corr = np.asarray(nii.dataobj)

    nii =  nb.load(SEED_CORR_THR)
    seed_corr_thr = np.asarray(nii.dataobj)
    idx = (seed_corr_thr == 0)

    # Only voxels that have significant correlation are considered
    print('Number of surviving voxels: {}'.format(np.sum(idx)))

    # Remove voxels q(pval) < 0.05
    seed_corr[idx] = 0
    seed_corr_avg = np.mean(seed_corr, axis=-1)
    seed_corr[seed_corr > 0 ] = 1
    seed_corr[seed_corr < 0 ] = -1
    #
    seed_corr = np.sum(seed_corr, axis=-1)


    # Read VMP
    header, data = bvbabel.vmp.read_vmp(REF_VMP)
    new_vmp_data = np.concatenate((data[..., None], seed_corr_avg[..., None], seed_corr[..., None]), axis=3)
    print(np.shape(new_vmp_data))

    # VMP preparation
    new_vmp_header = copy(header)
    new_vmp_header['NrOfSubMaps'] += 2

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][1]["MapName"] = '{} LAG 0 - correlation'.format(task)
    new_vmp_header["Map"][1]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 1], dtype=np.int32)
    new_vmp_header["Map"][1]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][1]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][1]["UpperThreshold"] = 0.8
    new_vmp_header["Map"][1]["MapThreshold"] = 0
    new_vmp_header["Map"][1]['LUTFileName']= '<default>'

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][2]["MapName"] = '{} LAG 0 - consistency'.format(task)
    new_vmp_header["Map"][2]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 2], dtype=np.int32)
    new_vmp_header["Map"][2]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][2]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][2]["UpperThreshold"] = 9
    new_vmp_header["Map"][2]["MapThreshold"] = 1
    new_vmp_header["Map"][2]['LUTFileName']= '<default>'

    # Save VMP
    basename = REF_VMP.split(os.extsep, 1)[0]
    OUTNAME = "{}_{}_GROUPSTAT_consistency_LAG{}.vmp".format(basename, task, LAG)
    bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
