"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives/"
MODELS = ['GLM_model1', 'GLM_model2']
THRESHOLD = 4
VOLUME = 10    # number of voxels (1.8 iso mm)

# Load Glasser VMP
VMP =  os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_MNI_bilateral_NATIVE_MANUAL.vmp')
header, data_atlas = bvbabel.vmp.read_vmp(VMP)
N_ROI = len(np.unique(data_atlas))

for it, model_type in enumerate(MODELS):
    print('Working on {}'.format(model_type))

    # Initiate output Dictionary
    ROI_dict = {"Phy_pref": [], "Amb_pref": [], "Both": [], "Phy_pref_count": [], "Amb_pref_count": [], "Both_count": []}

    roi_name_phy = []
    roi_name_amb = []
    roi_name_both = []

    roi_name_phy_count = []
    roi_name_amb_count = []
    roi_name_both_count = []

    # Read VMP
    VMP =  os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_conjunction_model{}_thre_{}.vmp'.format(it+1, THRESHOLD))
    header, data = bvbabel.vmp.read_vmp(VMP)   # Contains 3 value: 1--> physical; 2--> ambiguous; 3 --> both

    # Save NIFTI
    outname = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_conjunction_model{}_thre_{}_bvbabel.nii.gz'.format(it+1, THRESHOLD))
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
        count_phy = np.sum((data[idx_roi] == 1))
        count_amb = np.sum((data[idx_roi] == 2))
        count_both = np.sum((data[idx_roi] == 3))
        if roi == 203:
            print('ROI {} has {} voxels, phy {} amb {} both {}'.format(roi, roi_volume, count_phy, count_amb, count_both))

        if count_phy > VOLUME:
            roi_name_phy.append(roi)
            roi_name_phy_count.append(count_phy)
        if count_amb > VOLUME:
            roi_name_amb.append(roi)
            roi_name_amb_count.append(count_amb)

        if count_both > VOLUME:
            roi_name_both.append(roi)
            roi_name_both_count.append(count_both)

    # Add ROI list to each category
    ROI_dict['Phy_pref'] = roi_name_phy
    ROI_dict['Amb_pref'] = roi_name_amb
    ROI_dict['Both_pref'] = roi_name_both
    ROI_dict['Phy_pref_count'] = roi_name_phy_count
    ROI_dict['Amb_pref_count'] = roi_name_amb_count
    ROI_dict['Both_pref_count'] = roi_name_both_count

    print(roi_name_amb)
    print(roi_name_amb_count)

    # Save dictionary as an .npz file
    print('Save dictionary {}'.format(model_type))
    out = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_conjunction_model{}_thre_{}_dictionaryROI_{}_vox.npz'.format(it+1, THRESHOLD, VOLUME))
    np.savez(out, **ROI_dict)

print("Finished.")
