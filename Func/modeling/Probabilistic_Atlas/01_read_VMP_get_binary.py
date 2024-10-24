"""Read BrainVoyager VMP and apply a threshold_FDR"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ["sub-01", "sub-03", "sub-04","sub-05","sub-06","sub-07","sub-08","sub-09","sub-10"]
MODELS = ['GLM_model1', 'GLM_model2']
TASKS = ['phy', 'amb']

for it, model_type in enumerate(MODELS):

    for su in SUBJ:
        PATH_IN = os.path.join(STUDY_PATH, su,  'func', model_type, 'MultiRuns')

        for task in TASKS:
            print('Working on {} {} {}'.format(model_type, su, task))

            # Read VMP
            VMP =  os.path.join(PATH_IN, '{}_{}_model{}.vmp'.format(su, task, it+1))
            header, data = bvbabel.vmp.read_vmp(VMP)
            dims = np.shape(data)
            threshold_FDR = header['Map'][0]['FDRTableInfo'][1, 1]    # p < 0.05

            # Threshold the data
            data[data < threshold_FDR] = 0

            # Save binary map as VMP
            binary_map = np.zeros(dims)
            binary_map[data > 0] = 1

            # Adapt header
            header['Map'][0]['UpperThreshold'] = 1
            header['Map'][0]['MapThreshold'] = 0
            header['Map'][0]['ShowPosNegValues'] = 1
            header['Map'][0]['MapName'] = 'Binary map ({})'.format(task)

            outname =  os.path.join(PATH_IN, '{}_{}_model{}_FDR_binary.vmp'.format(su, task, it+1))
            bvbabel.vmp.write_vmp(outname, header, binary_map)


print("Finished.")
