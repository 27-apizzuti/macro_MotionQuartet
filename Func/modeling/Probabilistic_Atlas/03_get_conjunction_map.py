"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives/GroupStat"
MODELS = ['GLM_model1', 'GLM_model2']
THRESHOLD = 4

for it, model_type in enumerate(MODELS):

    # Initiate new data
    new_data = np.zeros([99, 127, 90])

    # Read VMP
    VMP =  os.path.join(STUDY_PATH, 'AllSbj_phy_model{}_FDR_probabilistic.vmp'.format(it+1))
    header, data_phy = bvbabel.vmp.read_vmp(VMP)
    VMP =  os.path.join(STUDY_PATH, 'AllSbj_amb_model{}_FDR_probabilistic.vmp'.format(it+1))
    header, data_amb = bvbabel.vmp.read_vmp(VMP)

    # Apply consistency across subjects as threshold
    data_phy[data_phy <= THRESHOLD] = 0      # This sets both < THRESHOLD and == 4 to 0
    data_amb[data_amb <= THRESHOLD] = 0      # This sets both < THRESHOLD and == 4 to 0

    # Binarize the maps
    data_phy[data_phy > 0] = 1
    data_amb[data_amb > 0] = 2

    # Sum the two binary map
    new_data = data_phy + data_amb

    # Adapt header
    print('Saving conjunction map for {}'.format(model_type))
    header['Map'][0]['UpperThreshold'] = 3
    header['Map'][0]['MapThreshold'] = 0.001
    header['Map'][0]['ShowPosNegValues'] = 1
    header['Map'][0] ['LUTFileName']= 'Preferences_3.olt'
    header['Map'][0]['MapName'] = 'Conjunction map (phy: 1, amb: 2, both: 3)'

    outname =  os.path.join(STUDY_PATH, 'AllSbj_conjunction_model{}_thre_{}.vmp'.format(it+1, THRESHOLD))
    bvbabel.vmp.write_vmp(outname, header, new_data)


print("Finished.")
