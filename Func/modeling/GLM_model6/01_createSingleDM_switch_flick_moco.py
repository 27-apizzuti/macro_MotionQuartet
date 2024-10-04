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
    PATH_GLM = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'GLM_model6')
    if not os.path.isdir(PATH_GLM):
        os.mkdir(PATH_GLM)

    for ru in RUNS:

        # // Find protocol file
        task = ru[0:3]
        runID = ru[3:5]

        print('Creating SDM for {} {}'.format(task, runID))

        if task == 'phy':
            PATH_PROTOCOL = os.path.join(STUDY_PATH, 'Protocols', su, 'Exp1_Phys_MotQuart', 'Protocols', 'Protocol_{}_Exp2_unamb_MotQuart_Run{}_model2.prt'.format(su, runID))
        else:
            PATH_PROTOCOL = os.path.join(STUDY_PATH, 'Protocols', su, 'Exp1_Amb_MotQuart', 'Protocols', 'Protocol_{}_Protocols_sess-03_Run{}_model2.prt'.format(su, runID))

        # // Find VTC file
        VTC_FILE = glob.glob(os.path.join(PATH_VTC, '*{}*run-{}*.vtc'.format(task, runID)))[0]

        # // Find MOTION PARAMETERS
        PATH_MOCO = os.path.join(STUDY_PATH,'derivatives', su, 'func', ru)

        # // Create SDM
        docVMR = brainvoyager.open(VMR_MNI)
        print('Linking {}'.format(VTC_FILE))
        docVMR.link_vtc(VTC_FILE)
        docVTC = brainvoyager.active_document
        nr_volumes = docVTC.n_volumes

        print('Linking protocol file {}'.format(PATH_PROTOCOL))
        docVMR.link_protocol(PATH_PROTOCOL)
        docVMR.clear_run_designmatrix()

        #// Set predictors
        docVMR.add_predictor("Switch")
        docVMR.set_predictor_values_from_condition("Switch", "Switch", 1)
        docVMR.apply_hrf_to_predictor("Switch")

        docVMR.add_predictor("Flicker")
        docVMR.set_predictor_values_from_condition("Flicker", "Flicker", 1)
        docVMR.apply_hrf_to_predictor("Flicker")

        # include constant as last predictor
        docVMR.add_predictor("Constant")
        docVMR.set_predictor_values("Constant", 1, nr_volumes, 1)

        # // Save SDM
        PATH_OUT = os.path.join(PATH_GLM,'SDM')
        if not os.path.isdir(PATH_OUT):
            os.mkdir(PATH_OUT)

        outname = os.path.join(PATH_OUT, '{}_{}_model6.sdm'.format(su, ru))
        docVMR.save_run_designmatrix(outname)

        # // Load again -- fix header no motions
        hdr, data = bvbabel.sdm.read_sdm(outname)
        hdr['IncludesConstant'] = 1

        bvbabel.sdm.write_sdm(outname, hdr, data)

        # // Load again -- add motion and fix header no motions
        hdr, data = bvbabel.sdm.read_sdm(outname)
        new_data = data[:-1]

        # Append motion parameters too
        cur_run_moco = glob.glob(os.path.join(PATH_MOCO, '*3DMC.sdm'))[0]
        print('Adding MOCO predictors {}'.format(cur_run_moco))
        hdr_moco, moco_data = bvbabel.sdm.read_sdm(cur_run_moco)

        for i, param in enumerate(moco_data):
            # param['ValuesOfPredictor'] = param['ValuesOfPredictor']
            # param['ValuesOfPredictor'] = zscore(param['ValuesOfPredictor'])
            new_data.append(param)
            print(np.shape(new_data))

        # Add constant
        new_data.append(data[-1])
        hdr['NrOfPredictors'] = len(new_data)
        hdr['IncludesConstant'] = 1
        hdr['FirstConfoundPredictor'] = len(new_data) - 6
        outname = os.path.join(PATH_OUT, '{}_{}_model6_MOCO.sdm'.format(su, ru))
        bvbabel.sdm.write_sdm(outname, hdr, new_data)
        docVMR.close()
