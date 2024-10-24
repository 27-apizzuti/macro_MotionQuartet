"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
import scipy.stats

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

model_type = 'GLM_model1'
dic_name = os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_amb_RFX_wSMOOTH_winner_map_pthreshold_GLASSER_control2.npz')

# Load the .npz file
mydict = np.load(dic_name)

# Access arrays in the loaded dictionary
print(len(mydict['Phy_pref']))
print(mydict['Amb_pref'])

with open("/mnt/e/WB-MotionQuartet/derivatives/GLM_model1/RFX_wSMOOTH/bilateral_Glasser_MNI_labels.txt", 'r') as f:
    lines = f.readlines()

res_txt = os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'results_comparison_control2.txt')
with open(res_txt, 'w') as f:
    f.write("Physical motion.\n")
    for roi in range(0, len(mydict['Phy_pref'])):
        roi_n = mydict['Phy_pref'][roi]
        f.write("{}".format(lines[roi_n-1]))
    f.write("\nAmbiguous motion.\n")
    for roi in range(0, len(mydict['Amb_pref'])):
        roi_n = mydict['Amb_pref'][roi]

        f.write("{}".format(lines[roi_n-1]))

# Only save bilateral activation
temp_amb = mydict['Amb_pref']
idx = temp_amb > 180
temp_amb[idx] = temp_amb[idx] - 180
unique, counts = np.unique(temp_amb, return_counts=True)
repeated_elements_amb = unique[counts > 1]

temp_phy = mydict['Phy_pref']
idx = temp_phy > 180
temp_phy[idx] = temp_phy[idx] - 180
unique, counts = np.unique(temp_phy, return_counts=True)
repeated_elements_phy = unique[counts > 1]

res_txt = os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'results_comparison_bilateral_control2.txt')
with open(res_txt, 'w') as f:
    f.write("Physical motion.\n")
    for roi in range(0, len(repeated_elements_phy)):
        roi_n = repeated_elements_phy[roi]
        f.write("{}".format(lines[roi_n-1]))
    f.write("\nAmbiguous motion.\n")
    for roi in range(0, len(repeated_elements_amb)):
        roi_n = repeated_elements_amb[roi]
        f.write("{}".format(lines[roi_n-1]))
