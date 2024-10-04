
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

STUDY_PATH = "/mnt/d/WB-MotionQuartet"
SUBJ = ["sub-09"]
SESS = [3]
TASK = ['amb02']

for su in SUBJ:
    for iterse, se in enumerate(SESS):
        print("Working on {} sess-{}".format(su, se))
        for tas in TASK:
            path_in = os.path.join(STUDY_PATH,  'derivatives', su, 'func', )
            runs = glob.glob("{}/{}*/".format(path_in, tas), recursive=True)
            print(runs)
            for path_run in runs:
                temp = path_run.split("/")[-2]

                if temp == 'phy00':
                    print('Skip {}'.format(temp))
                else:
                    PATH_TOPUP = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'topup')
                    PATH_ACQ = os.path.join(STUDY_PATH, 'derivatives', 'top-up_acq_tseries')

                    INPUT_AP = glob.glob(os.path.join(path_run, 'topup', '*3DMCTS_bvbabel.nii.gz'))[0]
                    print(INPUT_AP)
                    basename = INPUT_AP.split(os.extsep, 1)[0]
                    filename = basename.split("/")[-1]

                    nii = nb.load(INPUT_AP)
                    niidata = np.asarray(nii.dataobj)


                    tvol = np.shape(niidata)[-1]

                    # // Apply topup
                    # INPUT_AP = outname
                    print("Apply topup on {}".format(INPUT_AP))
                    TOPUP_RES = os.path.join(PATH_TOPUP, 'topup_results')
                    # // APPLY WITH PA PARAMS
                    if (su == 'sub-10') & (se == 2):
                        ACQ_AP = os.path.join(PATH_ACQ, "acqparams_PA_{}.txt".format(tvol))
                    else:
                        ACQ_AP = os.path.join(PATH_ACQ, "acqparams_AP_{}.txt".format(tvol))
                    OUT_AP = os.path.join(path_run, 'topup', "{}_undist.nii.gz".format(filename))

                    command = "applytopup -i {} -a {} --topup={} --inindex=1 --method=jac --interp=spline --verbose --out={} ".format(INPUT_AP, ACQ_AP, TOPUP_RES, OUT_AP)
                    subprocess.run(command, shell=True)
