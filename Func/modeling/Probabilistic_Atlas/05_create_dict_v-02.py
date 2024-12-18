"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives/"
TASKS = ['amb']
THRESHOLD = 4
VOLUME = 10    # number of voxels (1.8 iso mm)
COVERAGE = 5

# Load Glasser VMP
VMP =  os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_MNI_bilateral_NATIVE_MANUAL.vmp')
header, data_atlas = bvbabel.vmp.read_vmp(VMP)
N_ROI = len(np.unique(data_atlas))

for it, task_type in enumerate(TASKS):
    print('Working on {}'.format(task_type))

    # Initiate output Dictionary
    ROI_dict = {"Model1_pref": [], "Model2_pref": [], "Both": [], "Model1_pref_count": [], "Model2_pref_count": [], "Both_count": []}

    roi_name_m1 = []
    roi_name_m2 = []
    roi_name_both = []

    roi_name_m1_count = []
    roi_name_m2_count = []
    roi_name_both_count = []

    # Read VMP
    VMP =  os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_{}_task_conjunction_models_thre_{}.vmp'.format(task_type, THRESHOLD))
    header, data = bvbabel.vmp.read_vmp(VMP)   # Contains 3 value: 1--> model1 ; 2--> model2; 3 --> both

    # Save NIFTI
    outname = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_{}_task_conjunction_models_thre_{}_bvbabel.nii.gz'.format(task_type, THRESHOLD))
    img = nb.Nifti1Image(data, affine=np.eye(4))
    nb.save(img, outname)
    #
    for roi in range(1, N_ROI):

        # Flip labels
        if roi > 180:
            roi = roi - 180
        else:
            roi = roi + 180

        # Find voxels inside the ROI
        idx_roi = (data_atlas == roi)
        roi_volume = np.sum(idx_roi)
        count_1 = np.sum((data[idx_roi] == 1))
        count_2 = np.sum((data[idx_roi] == 2))
        count_both = np.sum((data[idx_roi] == 3))

        if roi == 203:
            print('ROI {} has {} voxels, phy {} amb {} both {}'.format(roi, roi_volume, count_1, count_2, count_both))

        if count_1 > VOLUME:
            if ((count_1/roi_volume)*100 > COVERAGE):
                print((count_1/roi_volume)*100)
                print(count_1)
                roi_name_m1.append(roi)
                roi_name_m1_count.append(count_1)
        if count_2 > VOLUME:
            if ((count_2/roi_volume)*100 > COVERAGE):
                roi_name_m2.append(roi)
                roi_name_m2_count.append(count_2)

        if count_both > VOLUME:
            if ((count_both/roi_volume)*100 > COVERAGE):
                roi_name_both.append(roi)
                roi_name_both_count.append(count_both)

    # Add ROI list to each category
    ROI_dict['Model1_pref'] = roi_name_m1
    ROI_dict['Model2_pref'] = roi_name_m2
    ROI_dict['Both_pref'] = roi_name_both
    ROI_dict['Model1_pref_count'] = roi_name_m1_count
    ROI_dict['Model2_pref_count'] = roi_name_m2_count
    ROI_dict['Both_pref_count'] = roi_name_both_count

    print(roi_name_m1)
    print(roi_name_m1_count)

    # Save dictionary as an .npz file
    print('Save dictionary {}'.format(task_type))
    out = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_{}_task_conjunction_models_thre_{}_dictionaryROI_{}_vox_COVERAGE.npz'.format(task_type, THRESHOLD, VOLUME))
    np.savez(out, **ROI_dict)

print("Finished.")
