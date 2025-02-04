""" Create single-subject design matrix for BrainVoyager GLM """

import bvbabel
import os
import numpy as np
import glob
from scipy.stats import zscore

SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
STUDY_PATH = 'E:\\WB-MotionQuartet'
VMR_MNI = os.path.join(STUDY_PATH, "derivatives", "MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr")
RUNS = ["phy01", "phy02", "amb01", "amb02", "amb03", "amb04"]
for su in SUBJ:

    PATH_VTC = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'VTC_MNI')
    PATH_GLM = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'GLM_model_2pred')
    PATH_OUT =  os.path.join(PATH_GLM,'SingleRun')

    if not os.path.isdir(PATH_GLM):
        os.mkdir(PATH_GLM)

    for ru in RUNS:

        # Task and run information
        task = ru[0:2]
        runID = ru[3:5]
        print('Computing GLM for {} {} {}'.format(su, task, runID))
        
        # VTC file
        VTC_FILE = glob.glob(os.path.join(PATH_VTC, '*{}*run-{}*.vtc'.format(task, runID)))[0]

        # SDM 
        SDM = os.path.join(PATH_GLM, 'SDM', '{}_{}_2preds_MOCO.sdm'.format(su, ru))

        # // Open VMR, link VTC
        docVMR = brainvoyager.open(VMR_MNI)   
        docVMR.link_vtc(VTC_FILE) 

        # // Run GLM  
        docVMR.load_run_designmatrix(SDM)
        docVMR.serial_correlation_correction_level = 2
        docVMR.compute_run_glm()
        docVMR.show_glm()
        docVMR.save_glm(os.path.join(PATH_OUT, '{}_{}_2preds_MOCO.glm'.format(su, ru)))
        docVMR.close()
