
"""
Created on Tue Apr  5 15:28:35 2022
    Convert anatomical nifti to VMR
@author: apizz

"""

import os
import glob


# =============================================================================
STUDY_PATH = 'D:\\Exp-MotionQuartet\\MRI_MQ\\BOLD'
# SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]
SUBJ = ["sub-09"]
SES = [2]

for su in SUBJ:
    for se in SES:
        PATH_IN = os.path.join(STUDY_PATH, su, 'sourcedata', 'sess-0{}'.format(se), 'NIFTI', 'anat')
        NIIS = glob.glob(os.path.join(PATH_IN, '*.nii'))
        print(NIIS)
        PATH_OUT = os.path.join(STUDY_PATH, su, 'derivatives', 'anat', '00_preps_MNI')
        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)
        PATH_OUT = os.path.join(PATH_OUT, 'anat')
        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)

        for nii in NIIS:
            print("Read {}".format(nii))
            basename = nii.split(os.extsep, 1)[0]
            filename = basename.split("/")[-1]
            outputname = os.path.join(PATH_OUT, '{}.vmr'.format(filename))
            print("Saving nifti as VMR: {}".format(outputname))

            #// Open nifti as VMR
            docVMR = bv.open(nii)
            docVMR.save_as(outputname)
