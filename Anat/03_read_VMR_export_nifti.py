"""Read BrainVoyager vmr and export nifti."""


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
# SUBJ = ["sub-01",  "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09"]
SUBJ = ["sub-09"]
FILES = ['sess-01_acq-mp2rage_UNI_denoised_IIHC_ISOpt6', 'sess-01_acq-mp2rage_inv2_ISOpt6']

for su in SUBJ:
    if su == 'sub-09':
        FILES = ['sess-02_acq-mp2rage_UNI_denoised_IIHC_ISOpt6', 'sess-02_acq-mp2rage_inv2_ISOpt6']
    print('Converting VMR anatomy for {}'.format(su))
    PATH_IN =os.path.join(STUDY_PATH,  su, 'derivatives', 'anat', '00_preps_MNI')

    for file in FILES:
        # VMR
        FILENAME = '{}_{}.vmr'.format(su, file)
        # FILENAME = '{}_ses-02_inv-2_part-mag_run-01_MP2RAGE_ISOpt6.vmr'.format(su)   # !!!! run-02 for sub-04, run-01  for the rest of the subjects
        FILE = os.path.join(PATH_IN, FILENAME)
        header, data = bvbabel.vmr.read_vmr(FILE)

        # Export nifti
        basename = FILENAME.split(os.extsep, 1)[0]
        outname = os.path.join(PATH_IN, "{}_bvbabel.nii.gz".format(basename))
        img = nb.Nifti1Image(data, affine=np.eye(4))
        nb.save(img, outname)

        # V16
        FILENAME = '{}_{}.v16'.format(su, file) # !!!! run-02 for sub-04, run-01 for the rest of the subjects
        # FILENAME = '{}_ses-0{}_uni_part-mag_run-01_MP2RAGE_denoised_IIHC_ISOpt6.v16'.format(su, SES[0])
        FILE = os.path.join(PATH_IN, FILENAME)
        header, data = bvbabel.v16.read_v16(FILE)

        # Export nifti
        basename = FILENAME.split(os.extsep, 1)[0]
        outname = os.path.join(PATH_IN, "{}_v16_bvbabel.nii.gz".format(basename))
        img = nb.Nifti1Image(data, affine=np.eye(4))
        nb.save(img, outname)

print("Finished.")
