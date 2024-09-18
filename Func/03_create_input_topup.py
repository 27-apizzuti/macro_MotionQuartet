
"""
Created on Tue Apr  5 15:28:35 2022
    Create topup input data (nifti)
    Only for phy00 and phy01
@author: apizz

"""

import os
import numpy as np
import nibabel as nb
import glob

STUDY_PATH = "/mnt/d/WB-MotionQuartet"
STUDY_PATH_SOURCE = "/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD"
SUBJ = ["sub-01", "sub-03", "sub-04","sub-05","sub-06","sub-07","sub-08","sub-09","sub-10"]
SESS = [3]

for su in SUBJ:

    for iterse, se in enumerate(SESS):
        print('Working on {} {} '.format(su, se))
        PATH_NIFTI = os.path.join(STUDY_PATH_SOURCE, su, 'sourcedata', 'sess-0{}'.format(se), 'NIFTI', 'func')
        PATH_TOPUP = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'topup')

        if not os.path.exists(PATH_TOPUP):
            os.mkdir(PATH_TOPUP)
        if (su == 'sub-10') & (se == 2):
            print('Main run are collected with PA')
            NIFTI_AP = "{}_sess-0{}_task-phy_acq-2depimb4_AP_run-00.nii".format(su, se)
            NIFTI_PA = "{}_sess-0{}_task-phy_acq-2depimb4_run-01.nii".format(su, se)
        else:
            NIFTI_AP = "{}_sess-0{}_task-phy_acq-2depimb4_run-01.nii".format(su, se)
            NIFTI_PA = "{}_sess-0{}_task-phy_acq-2depimb4_PA_run-00.nii".format(su, se)

        # // Load data
        # AP
        nii_AP = nb.load(os.path.join(PATH_NIFTI, NIFTI_AP))
        data_AP = np.asarray(nii_AP.dataobj)
        data_AP = data_AP[..., 0:5]

        outname = os.path.join(PATH_TOPUP, "{}_sess-0{}_AP.nii.gz".format(su, se))
        img = nb.Nifti1Image(data_AP, affine=nii_AP.affine, header=nii_AP.header)
        nb.save(img, outname)

        # PA
        nii_PA = nb.load(os.path.join(PATH_NIFTI, NIFTI_PA))
        data_PA = np.asarray(nii_PA.dataobj)
        data_PA = data_PA[..., 0:5]

        outname = os.path.join(PATH_TOPUP, "{}_sess-0{}_PA.nii.gz".format(su, se))
        img = nb.Nifti1Image(data_PA, affine=nii_PA.affine, header=nii_PA.header)
        nb.save(img, outname)

        new_data = np.concatenate((data_AP, data_PA), axis=-1)
        print(np.shape(new_data))

        # // Save
        outname = os.path.join(PATH_TOPUP, "{}_sess-0{}_updown_phase.nii.gz".format(su, se))
        img = nb.Nifti1Image(new_data, affine=nii_AP.affine, header=nii_AP.header)
        nb.save(img, outname)
