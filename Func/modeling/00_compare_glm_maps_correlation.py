"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

model_type = 'GLM_model2'

# Compute correlation between VMP maps from RFX model
# VMP_1 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_FFX_brainMask_sub-03_sub09.vmp')
VMP_1 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_RFX_wSMOOTH_brainMask.vmp')
header, data1 = bvbabel.vmp.read_vmp(VMP_1)
idx = data1 > 0
dims = np.shape(data1)
corr_reshaped = np.zeros(dims)

# Compute correlation between VMP maps from RFX model

# VMP_2 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_FFX_brainMask_sub-01_sub07.vmp')
VMP_2 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-amb_RFX_wSMOOTH_brainMask.vmp')
header, data2 = bvbabel.vmp.read_vmp(VMP_2)
corr = np.corrcoef(data1[idx], data2[idx])
print('Model1, Correlation between PHY and AMB (All Subject): {}'.format(corr[0, 1]))
#
# # ------------------ ADD CONTROL -----------------
# # Compute correlation between VMP maps from RFX model
# VMP_3 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_FFX_wSMOOTH_sub03_sub09_SMOOTH.vmp')
# header, data3 = bvbabel.vmp.read_vmp(VMP_3)
# corr = np.corrcoef(data1[idx], data3[idx])
# print('Model1, Correlation between PHY (All Subject) and PHY (Two Subjects): {}'.format(corr[0, 1]))
#
# corr = np.corrcoef(data2[idx], data3[idx])
# print('Model1, Correlation between AMB (All Subject) and PHY (Two Subjects): {}'.format(corr[0, 1]))
#
# print("Finished.")
