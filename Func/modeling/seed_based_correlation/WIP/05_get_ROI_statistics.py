"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from scipy import stats


STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
TASKS = ['amb', 'phy', 'rest']
# ROI_LIST = [1,4,5,6,15,21,22,25,28,43,44,45,46,47,55,59,84,107,117,144,147,148,149]
ROI_LIST = [86]
LAG = 2

for task in TASKS:
    for ROI in ROI_LIST:
        # Read VOI segmentation file
        ATLAS = "/mnt/e/WB-MotionQuartet/derivatives/Glasser_MNI_bilateral_NATIVE_MANUAL_vmp_1pt8_bvbabel.nii.gz"
        nii =  nb.load(ATLAS)
        atlas_data = np.asarray(nii.dataobj)
        idx_roi = (atlas_data == ROI)

        # Read probailistic group correlation map  LAG 0
        CORR = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR/AllSbj_amb_task_conjunction_models_thre_4_{}_GROUPSTAT_consistency_LAG0.vmp".format(task)
        header, data = bvbabel.vmp.read_vmp(CORR)
        corr = data[..., 2]

        # Find voxel of interest
        vox_mask = data[..., 0]
        idx_vox_green = (vox_mask == 2)
        idx = (idx_roi * idx_vox_green)
        # idx = idx_roi

        # Read probailistic group correlation map DRIVING
        CORR_LAG = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR/AllSbj_amb_task_conjunction_models_thre_4_{}_GROUPSTAT_follow_drive_consistency_LAG2_SEPARATEs.vmp".format(task, LAG)
        header, data = bvbabel.vmp.read_vmp(CORR_LAG)
        drive = data[..., 1]
        follow = data[..., 2]

        # Get stats
        stat1 = np.median(corr[idx])
        stat2 = np.median(drive[idx])
        stat3 = np.median(follow[idx])

        print('In {}, the seed MT+ with respect voxels in area {} shows:  correlation in {}/9, driving in {}/9, following in {}/9'.format(task, ROI, stat1, stat2, stat3))
    

print("Finished.")
