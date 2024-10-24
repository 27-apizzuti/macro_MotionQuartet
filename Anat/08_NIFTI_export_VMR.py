"""Read BrainVoyager vmr and export nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives/"
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']

for su in SUBJ:
    # Reference
    REF_VMR = os.path.join(STUDY_PATH, "MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr".format(su))
    NIFTI = os.path.join(STUDY_PATH, su, "anat", "00_preps_MNI", "ANTS", "{}_sess-01_uni_part-mag_run-01_MP2RAGE_denoised_IIHC_ISOpt6_SSbet_MNIWarped.nii.gz".format(su))

    # // VMR
    header, data = bvbabel.vmr.read_vmr(REF_VMR)
    print('Converting NIFTI to VMR')

    # Load nifti to convert
    nii =  nb.load(NIFTI)
    datanii = np.asarray(nii.dataobj).astype(np.uint16)

    outname = os.path.join(STUDY_PATH, su, "anat", "{}_sess-01_uni_part-mag_run-01_MP2RAGE_denoised_IIHC_ISOpt6_SSbet_MNIWarped.vmr".format(su))
    bvbabel.vmr.write_vmr(outname, header, datanii)
