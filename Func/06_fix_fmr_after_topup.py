
"""
Created on Tue Apr  5 15:28:35 2022
    Extract five volumes (topup)
@author: apizz

"""

import os
import numpy as np
import nibabel as nb
import subprocess
import glob

STUDY_PATH = "/mnt/d/WB-MotionQuartet/derivatives"
SUBJ = ["sub-09"]  # sub-09 and sub-08 rest
SESS = [3]
TASK = ["amb03", "amb04"]
# TASK = ["rest"]
for su in SUBJ:
    for iterse, se in enumerate(SESS):
        print("Working on {} sess-{}".format(su, se))
        for tas in TASK:
            path_in = os.path.join(STUDY_PATH, su, 'func')
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            print(runs)
            for path_run in runs:
                temp = path_run.split("/")[-2]

                if temp == 'phy00':
                    print('Skip {}'.format(temp))
                else:
                    PATH_TOPUP = os.path.join(STUDY_PATH, su, 'topup')

                    #//Load nifti to fix
                    if (su == "sub-01") & (se == 2):
                        INPUT_NII = glob.glob(os.path.join(path_run, 'topup', '*3DMCTS_bvbabel_undist_warped.nii.gz'))[0]
                        print("warped")
                    else:
                        INPUT_NII = glob.glob(os.path.join(path_run, 'topup', '*3DMCTS_bvbabel_undist.nii.gz'))[0]

                    print('Working on {} {} {}'.format(su, se, temp))
                    basename = INPUT_NII.split(os.extsep, 1)[0]
                    filename = basename.split("/")[-1]
                    print(filename)

                    nii = nb.load(INPUT_NII)
                    niidata = np.asarray(nii.dataobj)

                    #//Load reference nifti
                    nii2 = nb.load(os.path.join(path_in, "phy01", "{}_task-phy_acq-2depimb4_run-01_SCSTBL_3DMCTS.nii.gz".format(su)))
                    new_data = niidata[:,::-1,:,:]

                    #//Save new nifti
                    outname = os.path.join(path_run, 'topup', "{}_fix.nii.gz".format(filename))
                    img = nb.Nifti1Image(new_data, affine=nii2.affine, header=nii2.header)
                    nb.save(img, outname)
