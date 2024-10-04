""" Create single-subject design matrix for BrainVoyager GLM """

import bvbabel
import os
from pprint import pprint
import numpy as np
import glob
from scipy.stats import zscore
from copy import copy

SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
STUDY_PATH = 'E:\\WB-MotionQuartet'
VMR_MNI = os.path.join(STUDY_PATH, "derivatives", "MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr")
RUNS = ["phy01", "phy02", "amb01", "amb02", "amb03", "amb04"]


for su in SUBJ:

    for ru in RUNS:

        # // Find protocol file
        task = ru[0:3]
        runID = ru[3:5]

        print('Load PRT for {} {}'.format(task, runID))

        if task == 'phy':
            PATH_PROTOCOL = os.path.join(STUDY_PATH, 'Protocols', su, 'Exp1_Phys_MotQuart', 'Protocols', 'Protocol_{}_Exp2_unamb_MotQuart_Run{}.prt'.format(su, runID))
            # Load protocol
            header, data = bvbabel.prt.read_prt(PATH_PROTOCOL)

            # Apply modification
            print('Create switch predictor')
            switch = copy(data[1])
            switch['NameOfCondition'] = 'Switch'
            switch['Time start'] = np.sort(np.concatenate((data[1]['Time start'], data[2]['Time start']), axis=0))
            switch['NrOfOccurances'] = len(switch['Time start'])
            switch['Time stop'] = switch['Time start'] + 1

            # print(switch)
            print('Create sustained predictor')

            sust = copy(data[2])
            sust['NameOfCondition'] = 'Sustained'
            sust['Time start'] = switch['Time stop'] + 1
            sust['Time stop'] = np.sort(np.concatenate((data[1]['Time stop'], data[2]['Time stop']), axis=0))
            sust['NrOfOccurances'] = len(sust['Time start'])
            print(sust)

            print('Replace horizontal and vertical predictors with switch and sustained predictors')
            data[1] = copy(switch)
            data[2] = copy(sust)

            # Save PRT
            print('Save new protocol file')
            basename = PATH_PROTOCOL.split(os.extsep, 1)[0]
            outname = "{}_model2.prt".format(basename)
            bvbabel.prt.write_prt(outname, header, data)
        else:
            PATH_PROTOCOL = os.path.join(STUDY_PATH, 'Protocols', su, 'Exp1_Amb_MotQuart', 'Protocols', 'Protocol_{}_Protocols_sess-03_Run{}.prt'.format(su, runID))

            # Load protocol // This is in ms
            header, data = bvbabel.prt.read_prt(PATH_PROTOCOL)
            fix = data[0]
            flick = data[1]
            hor = data[2]
            ver = data[3]
            nuas = data[-1]
            print(hor['Time stop'])

            # Fix casting to integer
            fix['Time start'] = fix['Time start'].astype(int)
            fix['Time stop'] = fix['Time stop'].astype(int)
            flick['Time start'] = flick['Time start'].astype(int)
            flick['Time stop'] = flick['Time stop'].astype(int)
            nuas['Time start'] = nuas['Time start'].astype(int)
            nuas['Time stop'] = nuas['Time stop'].astype(int)

            # Apply modification
            print('Create switch predictor')
            switch = copy(data[2])
            switch['NameOfCondition'] = 'Switch'
            switch['Time start'] = np.sort(np.concatenate((hor['Time start'], ver['Time start']), axis=0)).astype(int)
            switch['Time stop'] = switch['Time start'] + int(1000)
            switch['NrOfOccurances'] = len(switch['Time start'])

            sust_end =  np.sort(np.concatenate((hor['Time stop'], ver['Time stop']), axis=0)).astype(int)

            # print(switch)
            print('Create sustained predictor')

            sust = copy(data[3])
            sust['NameOfCondition'] = 'Sustained'
            temp_start = switch['Time stop']
            sust['Time start'] = temp_start
            sust['Time stop'] = sust_end
            sust['NrOfOccurances'] = len(sust['Time start'])
            print(sust)

            print('Replace horizontal and vertical predictors with switch and sustained predictors')
            data[0] = copy(fix)
            data[1] = copy(switch)
            data[2] = copy(sust)
            data[3] = copy(flick)

            # Save PRT
            print('Save new protocol file')
            basename = PATH_PROTOCOL.split(os.extsep, 1)[0]
            outname = "{}_model2.prt".format(basename)
            bvbabel.prt.write_prt(outname, header, data)



        print("Finished.")
