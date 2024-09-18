"""Run ANTs to align single subject to MNI template. Both files are at 0.6 iso mm (TRX done within BV)."""


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import subprocess
from glob import glob

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'

SUBJ = ["sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]
SES = [1]

for su in SUBJ:
    for se in SES:
        if su == 'sub-09':
            se = 2
        print('Working on {}'.format(su))
        PATH_IN = os.path.join(STUDY_PATH,  su, 'derivatives', 'anat', '00_preps_MNI', 'ANTS')

        FILE_FIX = os.path.join(STUDY_PATH, 'MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6_bvbabel.nii.gz')
        FILE_MOV = glob(os.path.join(PATH_IN, '{}_sess-0{}_uni_part-mag_run-01_MP2RAGE_denoised_IIHC_ISOpt6_SSbet.nii.gz'.format(su, se)))[0]

        OUT = os.path.join(PATH_IN, '{}_sess-0{}_uni_part-mag_run-01_MP2RAGE_denoised_IIHC_ISOpt6_SSbet_MNI'.format(su, se))
        print('Running ANTS - Syn')

        #//0. Correct for inhomogeneities
        command = "antsRegistrationSyN.sh -d 3 -f {} -m {} -o {} -t s -n 12".format(FILE_FIX, FILE_MOV, OUT)
        subprocess.run(command, shell=True)

print("Finished.")
