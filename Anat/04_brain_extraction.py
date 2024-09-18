"""Read BrainVoyager vmr and export nifti."""


import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint
import subprocess

STUDY_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]
SES = [1]

for su in SUBJ:
    for se in SES:

        if su == 'sub-09':
            se = 2

        print('Working on {}'.format(su))
        PATH_IN = os.path.join(STUDY_PATH,  su, 'derivatives', 'anat', '00_preps_MNI')

        PATH_OUT = os.path.join(STUDY_PATH,  su, 'derivatives', 'anat', '00_preps_MNI', 'ANTS')
        if not os.path.exists(PATH_OUT):
            os.mkdir(PATH_OUT)

        FILE1 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_inv2_ISOpt6_bvbabel.nii.gz'.format(su, se))
        FILE2 = os.path.join(PATH_IN, '{}_sess-0{}_acq-mp2rage_UNI_denoised_IIHC_ISOpt6_bvbabel.nii.gz'.format(su, se))

        OUT1 = os.path.join(PATH_OUT, '{}_sess-0{}_acq-mp2rage_inv2_ISOpt6_bvbabel_BFC.nii.gz'.format(su, se))
        print('Running N4BiasFieldCorrection for INV2')

        #//0. Correct for inhomogeneities
        command = "N4BiasFieldCorrection -i {} ".format(FILE1)
        command += "-o {} ".format(OUT1)
        print(command)
        # subprocess.run(command, shell=True)

        print('Computing brainmask with BET')
        OUTBET = os.path.join(PATH_OUT, '{}_sess-0{}_mask_bet_mask.nii.gz'.format(su, se))
        command = "bet {} {} ".format(OUT1, OUTBET)
        command += "-m -R -f 0.03 "
        # subprocess.run(command, shell=True)


        #//2. Apply brainmask
        print('Apply brainmask')
        OUT3 = os.path.join(PATH_OUT, '{}_sess-0{}_uni_part-mag_run-01_MP2RAGE_denoised_IIHC_ISOpt6_SSbet.nii.gz'.format(su, se))
        command = "fslmaths {} -mas {} {} ".format(FILE2, OUTBET, OUT3)
        print(command)
        subprocess.run(command, shell=True)
        #
        #
        # #// BET again just for testing
        # print('Computing brainmask 2 with BET')
        # OUTBET2 = os.path.join(PATH_OUT, '{}_sess-0{}_mask_bet2.nii.gz'.format(su, se))
        # command = "bet {} {} ".format(OUT4, OUTBET2)
        # command += "-m -R -f 0.5 "
        # subprocess.run(command, shell=True)
        #
        # OUT5 = os.path.join(PATH_OUT, '{}_sess-0{}_uni_part-mag_run-02_MP2RAGE_denoised_IIHC_ISOpt6_SSbetx2.nii.gz'.format(su, se))
        #
        # command = "fslmaths {} -mas {} {} ".format(OUT4, OUTBET2, OUT5)
        # subprocess.run(command, shell=True)


print("Finished.")
