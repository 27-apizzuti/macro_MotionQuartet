"""Convert BrainVoyager VOI files into VTC sized Nifti files.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import bvbabel
import numpy as np
import nibabel as nb
from pprint import pprint
from glob import glob

# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
MAIN_PATH = '/mnt/e/WB-MotionQuartet/derivatives'
FILE_VOI = "/mnt/e/WB-MotionQuartet/derivatives/Glasser_atlas/alignment-BV-template_6pt/Glasser_MNI_bilateral_NATIVE.voi"
# =============================================================================

for su in SUBJ:
    print('Working on {}'.format(su))

    # Anatomical reference
    FILE_VMR = glob(os.path.join(MAIN_PATH, "MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6_NATIVE.vmr"))

    # Functional reference (output will be in in this space)
    FILE_VTC = glob(os.path.join(MAIN_PATH, su, 'func', 'VTC_MNI', '{}_task-phy_run-01_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc'.format(su)))
    OUTDIR = os.path.join(MAIN_PATH, su, 'func', 'GEC')

    # Output directory
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
        print("  Output directory: {}\n".format(OUTDIR))

    # -----------------------------------------------------------------------------
    # Step 1: Load voi
    header_voi, data_voi = bvbabel.voi.read_voi(FILE_VOI)

    # Print header information
    print("\nVOI header")
    for key, value in header_voi.items():
        print("  ", key, ":", value)

    # -----------------------------------------------------------------------------
    # Step 2: Get necessary information from VTC header
    header_vtc, data_vtc = bvbabel.vtc.read_vtc(FILE_VTC[0], rearrange_data_axes=False)

    # See header information
    print("\nVTC header")
    pprint(header_vtc)

    # Necessary header information
    vtc_scale   = header_vtc["VTC resolution relative to VMR (1, 2, or 3)"]

    # -----------------------------------------------------------------------------
    # Step 3: Get necessary information from VMR header
    header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR[0])

    # Print header nicely
    print("\nVMR header")
    for key, value in header_vmr.items():
        print(key, ":", value)

    # Necessary header information
    vmr_DimX = header_vmr["DimX"]
    vmr_DimY = header_vmr["DimY"]
    vmr_DimZ = header_vmr["DimZ"]

    # -----------------------------------------------------------------------------
    # Step 4: Generate a VTC sized nifti
    temp = np.zeros(data_vtc.shape[:-1])

    # Transpose axes
    temp = np.transpose(temp, [0, 2, 1])

    # -----------------------------------------------------------------------------
    # Step 5: Insert VOI into VTC sized Nifti
    for i in range(len(data_voi)):
        idx = data_voi[i]["Coordinates"]
        x = (idx[:, 0] - header_vtc['XStart']) // vtc_scale
        y = (idx[:, 1] - header_vtc['YStart']) // vtc_scale
        z = (idx[:, 2] - header_vtc['ZStart']) // vtc_scale
        temp[z, x, y] = i + 1  # +1 to skip zero

    # Flip axes
    temp = temp[::-1, ::-1, ::-1]

    # -----------------------------------------------------------------------------
    # Step 6: Export nifti
    filename = os.path.basename(FILE_VOI)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, f"{basename}_VOIinVTCspace.nii.gz")
    img = nb.Nifti1Image(temp, affine=np.eye(4))
    nb.save(img, outname)

print("\nFinished.")
