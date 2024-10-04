"""
Create VTC in NATIVE space
Final resolution VTC: 1.8 iso mm (original)
VMR: 1.6 iso mm

@author: apizz

"""

import numpy as np
import os
from glob import glob

print("Hello.")

# =============================================================================
STUDY_PATH = "E:\\WB-MotionQuartet\\derivatives"
SUBJ = ["sub-07"]
TASK = ["amb03"]

for su in SUBJ:
    
    VMR = glob(os.path.join(STUDY_PATH, su, 'anat', '00_preps_MNI', '*denoised_IIHC_ISOpt6.vmr'))[0]
    IA_TRX = glob(os.path.join(STUDY_PATH, su, 'func', 'BBR', '*IA.trf*'))[0]
    FA_TRX = glob(os.path.join(STUDY_PATH, su, 'func', 'BBR', '*BBR_FA.trf'))[0]
    PATH_IN = os.path.join(STUDY_PATH, su, 'func')
    
    #PATH_IN = os.path.join('F:\\Motion_Quartet_derivatives', '{}'.format(su), 'sess-03')
    PATH_OUT =  os.path.join(STUDY_PATH, su, 'func', 'VTC_native')
    
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)

    for tas in TASK:
        runs = glob("{}\\{}*\\".format(PATH_IN, tas), recursive=True)
        print(runs)
        for path_run in runs:
            print(path_run)
            temp = path_run.split("\\")[-2]
            print(temp)
            if temp == 'phy00':
                print("Skip")
            else:

                #// Open VMR
                doc_vmr = bv.open(VMR)

                #// Input files
                fmr_file = glob(os.path.join(path_run, 'topup','*_undist_fix_THPGLMF3c.fmr'))[0]
                coreg_fa_trf_file = FA_TRX
                coreg_ia_trf_file = IA_TRX
                
                print(fmr_file)

                #// Output name
                basename = fmr_file.split(os.extsep, 1)[0]
                outname = basename.split("\\")[-1]
                vtc_file = os.path.join(PATH_OUT, "{}_BBR_native.vtc".format(outname))
                doc_vmr.create_vtc_in_native_space(fmr_file, coreg_ia_trf_file, coreg_fa_trf_file, vtc_file, 3, 2)

                #// 1 means we are using trilinear interpolation (SINC option was crushing)
                #// 2 means we are using sinc interpolation (TODO: Discuss which interpolation has to be used)
