"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
import scipy.stats

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

model_type = 'GLM_model1'

# Winner map
VMP_1 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_amb_RFX_wSMOOTH_winner_map_pthreshold_control2.vmp')
header, data1 = bvbabel.vmp.read_vmp(VMP_1)
print(np.unique(data1))
idx = data1 > 0
dims = np.shape(data1)
print(dims)

# Load Glasser VMP
VMP_2 =  os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_MNI_bilateral_NATIVE_MANUAL.vmp')
header2, data2 = bvbabel.vmp.read_vmp(VMP_2)
N_ROI = len(np.unique(data2))
new_data = np.zeros(dims)
ROI_dict = {"Phy_pref": [], "Amb_pref": []}
roi_name_phy = []
roi_name_amb = []

for roi in range(1, N_ROI):
    idx_roi = (data2 == roi)
    roi_coverage = np.sum(idx_roi*idx) / np.sum(idx_roi)
    # print(roi_coverage)
    if roi_coverage > 0.1:
        count1 = np.sum((data1[idx_roi*idx] == 1))
        count2 = np.sum((data1[idx_roi*idx] == 2))

        if count1 > count2:
            new_data[idx_roi] = 1
            roi_name_phy.append(roi)
        else:
            new_data[idx_roi] = 2
            roi_name_amb.append(roi)
    # else:
    #     # print('Skip ROI')
print(roi_name_phy)
print(roi_name_amb)
ROI_dict['Phy_pref'] = roi_name_phy
ROI_dict['Amb_pref'] = roi_name_amb

# Save dictionary as an .npz file
out = os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_amb_RFX_wSMOOTH_winner_map_pthreshold_GLASSER_control2.npz')
np.savez(out, **ROI_dict)

# Adapt header
header2['Map'][0]['LUTFileName'] = 'Preferences_2.olt'
header2['Map'][0]['UpperThreshold'] = 2
header2['Map'][0]['MapThreshold'] = 0
header2['Map'][0]['MapName'] = 'Winner map (1:phy, 2:amb)'

outname =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_amb_RFX_wSMOOTH_winner_map_pthreshold_GLASSER_controls2.vmp')
bvbabel.vmp.write_vmp(outname, header2, new_data)

print("Finished.")
