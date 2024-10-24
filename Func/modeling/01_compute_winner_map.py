"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

model_type = 'GLM_model2'
# t_thr = 3.5
t_thr = 2.57

# Physical VMP maps from RFX model
VMP_1 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_FFX_brainMask_sub-01_sub07.vmp')
# VMP_1 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_RFX_wSMOOTH_brainMask.vmp')
header, data1 = bvbabel.vmp.read_vmp(VMP_1)
dims = np.shape(data1)
pprint(header)

# Ambiguous VMP maps from RFX model
VMP_2 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-amb_FFX_brainMask_sub-01_sub07.vmp')
# VMP_2 =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-amb_RFX_wSMOOTH_brainMask.vmp')
header, data2 = bvbabel.vmp.read_vmp(VMP_2)

# // Save unthreshold winenr map
idx1 = data1 > data2
idx2 = data2 > data1

winner_map = np.zeros(dims)
winner_map[idx1] = 1
winner_map[idx2] = 2

# Adapt header
header['Map'][0]['LUTFileName'] = 'Preferences_2.olt'
header['Map'][0]['UpperThreshold'] = 2
header['Map'][0]['MapThreshold'] = 0
header['Map'][0]['MapName'] = 'Winner map (1:phy, 2:amb)'

outname =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_amb_RFX_wSMOOTH_winner_map_unthresholded_control2.vmp')
bvbabel.vmp.write_vmp(outname, header, winner_map)

# Threshold VMP according to p-value
winner_map = np.zeros(dims)

data1[data1 < t_thr] = 0
data2[data2 < t_thr] = 0

idx1 = data1 > data2
idx2 = data2 > data1
winner_map[idx1] = 1
winner_map[idx2] = 2

# Adapt header
header['Map'][0]['LUTFileName'] = 'Preferences_2.olt'
header['Map'][0]['UpperThreshold'] = 2
header['Map'][0]['MapThreshold'] = 0
header['Map'][0]['MapName'] = 'Winner map (1:phy, 2:amb)'

outname =  os.path.join(STUDY_PATH, model_type, 'RFX_wSMOOTH', 'task-phy_amb_RFX_wSMOOTH_winner_map_pthreshold_control2.vmp')
bvbabel.vmp.write_vmp(outname, header, winner_map)

print("Finished.")
