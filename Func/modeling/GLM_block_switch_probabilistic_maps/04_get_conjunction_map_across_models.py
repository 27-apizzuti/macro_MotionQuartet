"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat"
TASKS = ['phy', 'amb']
THRESHOLD = 4

for it, task_type in enumerate(TASKS):

    # Initiate new data
    new_data = np.zeros([99, 127, 90])

    # Read VMP
    VMP =  os.path.join(STUDY_PATH, 'AllSbj_{}_model1_FDR_probabilistic.vmp'.format(task_type))
    header, data_model1 = bvbabel.vmp.read_vmp(VMP)
    VMP =  os.path.join(STUDY_PATH, 'AllSbj_{}_model2_FDR_probabilistic.vmp'.format(task_type))
    header, data_model2 = bvbabel.vmp.read_vmp(VMP)

    # Apply consistency across subjects as threshold
    data_model1[data_model1 <= THRESHOLD] = 0      # This sets both < THRESHOLD and == 4 to 0
    data_model2[data_model2 <= THRESHOLD] = 0      # This sets both < THRESHOLD and == 4 to 0

    # Binarize the maps
    data_model1[data_model1 > 0] = 1
    data_model2[data_model2 > 0] = 2

    # Sum the two binary map
    new_data = data_model1 + data_model2

    # Adapt header
    print('Saving conjunction map for {}'.format(task_type))
    header['Map'][0]['UpperThreshold'] = 3
    header['Map'][0]['MapThreshold'] = 0.001
    header['Map'][0]['ShowPosNegValues'] = 1
    header['Map'][0] ['LUTFileName']= 'Preferences_3.olt'
    header['Map'][0]['MapName'] = 'Conjunction map {} (model1: 1, model2: 2, both: 3)'.format(task_type)

    outname =  os.path.join(STUDY_PATH, 'AllSbj_{}_task_conjunction_models_thre_{}.vmp'.format(task_type, THRESHOLD))
    bvbabel.vmp.write_vmp(outname, header, new_data)


print("Finished.")
