
"""
Created on Tue Apr  5 15:28:35 2022
    Resample anatomy from 0.7 to 0.6 ISO mm in BrainVoyager
    This is advantageous since we can create the VTC at its original resolution 1.8 and overlay to 0.6 anat
    (VMR resolution x3)
@author: apizz

"""

import os
import glob

# =============================================================================
STUDY_PATH = 'D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD'
# SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]
SUBJ = ['sub-09']
FILES = ['sess-01_acq-mp2rage_UNI_denoised_IIHC', 'sess-01_acq-mp2rage_inv2']

for su in SUBJ:
    if su == 'sub-09':
        FILES = ['sess-02_acq-mp2rage_UNI_denoised_IIHC', 'sess-02_acq-mp2rage_inv2']

    PATH_IN = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', '00_preps_MNI')
    for file in FILES:
        fileVMR = glob.glob(os.path.join(PATH_IN, '{}_{}.vmr'.format(su, file)))[0]
        basename = fileVMR.split(os.extsep, 1)[0]
        OUTPUTNAME = '{}_ISOpt6.vmr'.format(basename)
        print("Open VMR: {}".format(fileVMR))

        #// Open nifti as VMR
        docVMR = bv.open(fileVMR)
        docVMR.transform_to_isovoxel(0.6, 512, 3, OUTPUTNAME)
