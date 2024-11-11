"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from scipy import stats
from copy import copy

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
TASKS = ['amb', 'phy', 'rest']
# ROI_LIST = [1,4,5,6,15,21,22,25,28,43,44,45,46,47,55,59,84,107,117,144,147,148,149]
ROI_LIST = [86]
LAG = 2

for task in TASKS:

    # Read probailistic group correlation map  LAG 0
    CORR = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR/AllSbj_amb_task_conjunction_models_thre_4_{}_GROUPSTAT_consistency_LAG0.vmp".format(task)
    header, data = bvbabel.vmp.read_vmp(CORR)
    corr = data[..., 2]

    # Find voxel of interest
    vox_mask = data[..., 0]
    idx_vox_green = (vox_mask == 2)

    # Read probailistic group correlation map DRIVING
    CORR_LAG = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR/AllSbj_amb_task_conjunction_models_thre_4_{}_GROUPSTAT_follow_drive_consistency_LAG{}_SEPARATE.vmp".format(task, LAG)
    header, data = bvbabel.vmp.read_vmp(CORR_LAG)
    drive = data[..., 1]
    follow = data[..., 2]

    # Get stats
    stat1 = np.zeros(np.shape(corr))
    stat2 = np.zeros(np.shape(corr))
    stat3 = np.zeros(np.shape(corr))

    stat1[idx_vox_green] = corr[idx_vox_green]
    stat2[idx_vox_green] = drive[idx_vox_green]
    stat3[idx_vox_green] = follow[idx_vox_green]

    # Save new VMP maps only with the green voxels
    # VMP preparation
    new_vmp_header = copy(header)
    new_vmp_data = np.concatenate((data, stat1[..., None], stat2[..., None], stat3[..., None]), axis=3)

    new_vmp_header['NrOfSubMaps'] += 3

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][3]["MapName"] = 'Correlation LAG 0 - consistency'.format(task)
    new_vmp_header["Map"][3]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 3], dtype=np.int32)
    new_vmp_header["Map"][3]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][3]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][3]["UpperThreshold"] = 9
    new_vmp_header["Map"][3]["MapThreshold"] = 1
    new_vmp_header["Map"][3]['LUTFileName']= '<default>'

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][4]["MapName"] = 'Driving LAG {} - consistency'.format(LAG)
    new_vmp_header["Map"][4]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 4], dtype=np.int32)
    new_vmp_header["Map"][4]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][4]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][4]["UpperThreshold"] = 9
    new_vmp_header["Map"][4]["MapThreshold"] = 1
    new_vmp_header["Map"][4]['LUTFileName']= 'ProbMap_Red.olt'

    new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
    new_vmp_header["Map"][5]["MapName"] = 'Following {} - consistency'.format(LAG)
    new_vmp_header["Map"][5]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 5], dtype=np.int32)
    new_vmp_header["Map"][5]["EnableClusterSizeThreshold"] = 0
    new_vmp_header["Map"][5]["ShowPosNegValues"] = 1
    new_vmp_header["Map"][5]["UpperThreshold"] = 9
    new_vmp_header["Map"][5]["MapThreshold"] = 1
    new_vmp_header["Map"][5]['LUTFileName']= 'ProbMap_Blue.olt'


    # Save VMP
    basename = CORR_LAG.split(os.extsep, 1)[0]
    OUTNAME = "{}_visual_surface.vmp".format(basename)
    bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)


print("Finished.")
