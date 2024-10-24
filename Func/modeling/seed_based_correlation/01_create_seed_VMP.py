"""Create seed within the MT+ complex."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
from copy import copy
ROIS = [2, 23, 156, 157]   # MST, MT, V4t, FST

MODEL = 'model2'

VMP_REF = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/AllSbj_conjunction_{}_thre_4.vmp".format(MODEL)
GLASSER_FILE = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/seed_based_correlation/nifti/Glasser_MNI_bilateral_NATIVE_MANUAL_vmp_bvbabel.nii.gz"
GROUP_MAP = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/seed_based_correlation/nifti/AllSbj_conjunction_{}_thre_4_bvbabel.nii.gz".format(MODEL)

# =============================================================================
# Load nifti
nii =  nb.load(GLASSER_FILE)
seg_glasser = np.asarray(nii.dataobj)
idx_glasser = np.zeros(np.shape(seg_glasser))

for roi in ROIS:
    idx_glasser = idx_glasser + (seg_glasser == roi) + (seg_glasser == (roi + 180))

# Save SEED
outname = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/seed_based_correlation/nifti/Glasser_MNI_bilateral_NATIVE_MANUAL_vmp_bvbabel_SEED_MT_plus.nii.gz"
img = nb.Nifti1Image(idx_glasser, affine=np.eye(4))
nb.save(img, outname)


# Find group-surviving voxels inside the seed-ROI
nii =  nb.load(GROUP_MAP)
group = np.asarray(nii.dataobj)
idx = group > 1

# Voxel-mask
idx_group = idx * idx_glasser

# Save group voxels
outname = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/seed_based_correlation/nifti/AllSbj_conjunction_model2_thre_4_bvbabel_SEED_MT_plus.nii.gz"
img = nb.Nifti1Image(idx_group, affine=np.eye(4))
nb.save(img, outname)

# ---------------------
# Save as extra maps in the VMP file
header, data = bvbabel.vmp.read_vmp(VMP_REF)
new_vmp_data = np.concatenate((data[..., None], idx_glasser[..., None], idx_group[..., None]), axis=3)
print(np.shape(new_vmp_data))

# VMP preparation
new_vmp_header = copy(header)
new_vmp_header['NrOfSubMaps'] += 2
new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][1]["MapName"] = 'MT+ seed'
new_vmp_header["Map"][1]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 1], dtype=np.int32)
new_vmp_header["Map"][1]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][1]["ShowPosNegValues"] = 1
new_vmp_header["Map"][1]["UpperThreshold"] = np.max(new_vmp_data[..., 1])
new_vmp_header["Map"][1]["MapThreshold"] = np.min(new_vmp_data[..., 1])

new_vmp_header["Map"].append(copy(new_vmp_header["Map"][0]))
new_vmp_header["Map"][2]["MapName"] = 'group voxels within MT+ seed'
new_vmp_header["Map"][2]["NrOfUsedVoxels"] = np.sum(new_vmp_data[..., 2], dtype=np.int32)
new_vmp_header["Map"][2]["EnableClusterSizeThreshold"] = 0
new_vmp_header["Map"][2]["ShowPosNegValues"] = 1
new_vmp_header["Map"][2]["UpperThreshold"] = np.max(new_vmp_data[..., 2])
new_vmp_header["Map"][2]["MapThreshold"] = np.min(new_vmp_data[..., 2])

# Save VMP
basename = VMP_REF.split(os.extsep, 1)[0]
OUTNAME = "{}_SEED_MT_plus.vmp".format(basename, roi)
bvbabel.vmp.write_vmp(OUTNAME, new_vmp_header, new_vmp_data)
print("Finished.")
