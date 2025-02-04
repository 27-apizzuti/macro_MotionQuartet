"""Read BrainVoyager GLM and export Nifti."""

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
    for task in TASKS:
        new_data = np.zeros([99, 127, 90])
        for su in SUBJ:
            PATH_IN = os.path.join(STUDY_PATH, su,  'func', model_type, 'MultiRuns')
            # Read VMP
            VMP =  os.path.join(PATH_IN, '{}_{}_model{}_FDR_binary.vmp'.format(su, task, it+1))
            header, data = bvbabel.vmp.read_vmp(VMP)
            new_data = new_data + data

        # Adapt header
        print('Saving probabilistic map for {} {}'.format(model_type, task))
        header['Map'][0]['UpperThreshold'] = len(SUBJ)
        header['Map'][0]['MapThreshold'] = 0
        header['Map'][0]['ShowPosNegValues'] = 1
        header['Map'][0]['MapName'] = 'Probabilistic map ({})'.format(task)

        outname =  os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_{}_model{}_FDR_probabilistic.vmp'.format(task, it+1))
        bvbabel.vmp.write_vmp(outname, header, new_data)


print("Finished.")
