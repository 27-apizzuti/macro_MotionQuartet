"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

# Load Reference VMP
FILE = os.path.join(STUDY_PATH, 'GLM_model1', 'RFX_wSMOOTH', 'task-phy_RFX_wSMOOTH_brainMask.vmp')
header, data = bvbabel.vmp.read_vmp(FILE)
data_vmp = np.zeros(np.shape(data))

# LOAD VMP
FILE1 = os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_LH.vmp')
header1, data1 = bvbabel.vmp.read_vmp(FILE1)

FILE2 = os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_RH.vmp')
header2, data2 = bvbabel.vmp.read_vmp(FILE2)
idx = data2 > 0
data2[idx] = data2[idx] + 180
new_data = data1 + data2

# Put the value inside the small matrix
data_vmp = new_data[header['ZEnd']:header['ZEnd'], header['XEnd']:header['XEnd'], header['YEnd']:header['YEnd']]

# Save VMP
outputname = os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_MNI_bilateral_SMALL.vmp')
bvbabel.vmp.write_vmp(outputname, header, new_data)
