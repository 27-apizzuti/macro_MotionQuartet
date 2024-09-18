"""BBR in BrainVoyager
@author: apizz """

import os
import numpy as np
import glob

#// Set input
STUDY_PATH = "D:\\WB-MotionQuartet\\derivatives"
#SUBJ = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-11"]
SUBJ = ["sub-01"]

for su in SUBJ:
        PATH_IN = os.path.join(STUDY_PATH, su)
        fmr_file = glob.glob(os.path.join(PATH_IN, 'func', 'phy01', 'topup', '*THP*.fmr'))[0]
        print(fmr_file)
        vmr_file = os.path.join(PATH_IN, 'anat', '00_preps_MNI', 'sub-01_sess-01_acq-mp2rage_UNI_denoised_IIHC_ISOpt6.vmr')
        print("Run BBR on {} using anat ".format(fmr_file))
        # // Run BBR
        doc_vmr = bv.open(vmr_file)
        doc_vmr = bv.active_document
        doc_vmr.coregister_fmr_to_vmr_using_bbr(fmr_file)

print("Finished.")
