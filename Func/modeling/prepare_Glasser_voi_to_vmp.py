"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"

# Load Reference VMP
FILE = os.path.join(STUDY_PATH, 'GLM_model1', 'RFX_wSMOOTH', 'task-phy_RFX_wSMOOTH_brainMask.vmp')
header_vmp, data_vmp = bvbabel.vmp.read_vmp(FILE)
vmp_scale = header_vmp['Resolution']

# Step 1: Load voi
FILE_VOI = os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_MNI_bilateral_NATIVE.voi')
header_voi, data_voi = bvbabel.voi.read_voi(FILE_VOI)

# Print header information
print("\nVOI header")
for key, value in header_voi.items():
    print("  ", key, ":", value)

# -----------------------------------------------------------------------------
# Step 4: Generate a VTC sized nifti
temp = np.zeros(np.shape(data_vmp))

# -----------------------------------------------------------------------------
# Step 5: Insert VOI into VTC sized Nifti
for i in range(len(data_voi)):
    idx = data_voi[i]["Coordinates"]
    x = ((idx[:, 0] - header_vmp['ZStart']) // vmp_scale)
    y = ((idx[:, 1] - header_vmp['XStart']) // vmp_scale)
    z = ((idx[:, 2] - header_vmp['YStart']) // vmp_scale)
    # temp[z-4, x+4, y-4] = i + 1  # +1 to skip zero
    temp[z, x, y] = i + 1
# Flip axes
temp = temp[:, ::-1, ::-1]
print(np.shape(temp))
outname = os.path.join(STUDY_PATH, 'Glasser_atlas', 'alignment-BV-template_6pt', 'Glasser_MNI_bilateral_NATIVE_TEST.vmp')
bvbabel.vmp.write_vmp(outname, header_vmp, temp)
