# preprocess FMR: highpass ; @author: apizz
# This script was used to preprocess high-res and lo-res functional data acquired with CMRR sequence;

import numpy as np
import os
import glob

print("Hello.")

# =============================================================================
STUDY_PATH = "D:\\WB-MotionQuartet\\derivatives"
SUBJ = ["sub-01"]
TASK = ["rest01"]

HPF_CUTOFF = 3

for su in SUBJ:
    
    PATH_IN = os.path.join(STUDY_PATH, su, 'func')
    print(PATH_IN)
    
    for tas in TASK:
        runs = glob.glob("{}\\{}*\\".format(PATH_IN, tas), recursive=True)
        print(runs)
        for path_run in runs:
            print(path_run)
            temp = path_run.split("\\")[-2]
            print(temp)
            if temp == 'phy00':
                print("Skip")
            else:

                print("Run HPF for {}".format(path_run))
                ru = glob.glob(os.path.join(path_run, 'topup', '*undist_fix.nii.gz'))[0]
                
                # // Open nifti and save fmri
                docnii=bv.open(ru)
                docnii.close()

                # // High-pass filtering
                docnii=bv.open(ru)
                docnii.filter_temporal_highpass_glm_fourier(HPF_CUTOFF)
                docnii.close()
