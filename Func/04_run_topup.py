
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
SUBJ = ["sub-01", "sub-03", "sub-04","sub-05","sub-06","sub-07","sub-08","sub-09","sub-10"]
SESS = [3]

for su in SUBJ:
    for iterse, se in enumerate(SESS):
        print("Working on {} sess-{}".format(su, se))

        PATH_TOPUP = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'topup')

        # // Run topup
        INPUT_FILE = os.path.join(PATH_TOPUP, "{}_sess-0{}_updown_phase.nii.gz".format(su, se))
        PARAMS = os.path.join(PATH_TOPUP, 'acqparams.txt')
        CONFIG = os.path.join(PATH_TOPUP, 'b0_conf.cnf')
        topup_results = os.path.join(PATH_TOPUP, 'topup_results')

        print("Topup is running")
        command = "topup --imain={} --datain={} --config={} --out={}".format(INPUT_FILE, PARAMS, CONFIG, topup_results)
        subprocess.run(command, shell=True)
        print("Topup is computed")

        # // Apply topup
        TOPUP_RES = os.path.join(PATH_TOPUP, 'topup_results')
        INPUT_AP = os.path.join(PATH_TOPUP, "{}_sess-0{}_AP.nii.gz".format(su, se))
        ACQ_AP = os.path.join(PATH_TOPUP, "acqparams_AP.txt")
        OUT_AP = os.path.join(PATH_TOPUP, "{}_sess-0{}_AP_undist.nii.gz".format(su, se))

        command = "applytopup -i {} -a {} --topup={} --inindex=1 --method=jac --interp=spline --verbose --out={} ".format(INPUT_AP, ACQ_AP, TOPUP_RES, OUT_AP)
        subprocess.run(command, shell=True)

        # // Apply topup PA
        INPUT_PA = os.path.join(PATH_TOPUP, "{}_sess-0{}_PA.nii.gz".format(su, se))
        ACQ_PA = os.path.join(PATH_TOPUP, "acqparams_PA.txt")
        OUT_PA = os.path.join(PATH_TOPUP, "{}_sess-0{}_PA_undist.nii.gz".format(su, se))

        command = "applytopup -i {} -a {} --topup={} --inindex=1 --method=jac --interp=spline --verbose --out={} ".format(INPUT_PA, ACQ_PA, TOPUP_RES, OUT_PA)
        subprocess.run(command, shell=True)
