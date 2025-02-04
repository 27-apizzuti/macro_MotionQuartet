"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
import scipy.stats

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
THRESHOLD = 4
MODELS = ['GLM_model1', 'GLM_model2']
VOLUME = 10

for it, model_type in enumerate(MODELS):

    print('Working on {}'.format(model_type))
    DIC_NAME = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_conjunction_model{}_thre_{}_dictionaryROI_{}_vox.npz'.format(it+1, THRESHOLD, VOLUME))

    # Load the .npz file
    mydict = np.load(DIC_NAME)

    # Access arrays in the loaded dictionary
    print('There are {} ROIs preferring physical '.format(len(mydict['Phy_pref'])))
    print('There are {} ROIs preferring ambiguous '.format(len(mydict['Amb_pref'])))
    print('There are {} ROIs preferring both '.format(len(mydict['Both_pref'])))

    # Open Glasser names
    with open("/mnt/e/WB-MotionQuartet/derivatives/GLM_model1/RFX_wSMOOTH/bilateral_Glasser_MNI_labels.txt", 'r') as f:
        lines = f.readlines()

    # Output file
    basename = DIC_NAME.split(os.extsep, 1)[0]
    res_txt = "{}_NAMES.txt".format(basename)

    # print('For physical, I am writing ROI: {} with {} voxels'.format(roi_n, mydict['Phy_pref_count'][roi]))
    with open(res_txt, 'w') as f:
        f.write("Physical motion.\n")
        for roi in range(0, len(mydict['Phy_pref'])):
            roi_n = mydict['Phy_pref'][roi]
            f.write("{}, {}\n".format(lines[roi_n-1].strip(), str(mydict['Phy_pref_count'][roi])))
        f.write("\nAmbiguous motion.\n")

        for roi in range(0, len(mydict['Amb_pref'])):
            roi_n = mydict['Amb_pref'][roi]
            f.write("{}, {}\n".format(lines[roi_n-1].strip(), str(mydict['Amb_pref_count'][roi])))
        f.write("\nBoth.\n")

        for roi in range(0, len(mydict['Both_pref'])):
            roi_n = mydict['Both_pref'][roi]
            f.write("{}, {}\n".format(lines[roi_n-1].strip(), str(mydict['Both_pref_count'][roi])))

    # Only save bilateral activation
    temp_amb = mydict['Amb_pref']

    idx = temp_amb > 180
    temp_amb[idx] = temp_amb[idx] - 180
    unique, counts = np.unique(temp_amb, return_counts=True)
    repeated_elements_amb = unique[counts > 1]

    temp_phy = mydict['Phy_pref']
    idx = temp_phy > 180
    temp_phy[idx] = temp_phy[idx] - 180
    unique, counts = np.unique(temp_phy, return_counts=True)
    repeated_elements_phy = unique[counts > 1]

    temp_both = mydict['Both_pref']
    idx = temp_both > 180
    temp_both[idx] = temp_both[idx] - 180
    unique, counts = np.unique(temp_both, return_counts=True)
    repeated_elements_both = unique[counts > 1]

    res_txt = "{}_NAMES_BILATERAL.txt".format(basename)
    with open(res_txt, 'w') as f:
        f.write("Physical motion.\n")
        for roi in range(0, len(repeated_elements_phy)):
            roi_n = repeated_elements_phy[roi]
            f.write("{}".format(lines[roi_n-1]))
        f.write("\nAmbiguous motion.\n")
        for roi in range(0, len(repeated_elements_amb)):
            roi_n = repeated_elements_amb[roi]
            f.write("{}".format(lines[roi_n-1]))
        f.write("\nBoth.\n")
        for roi in range(0, len(repeated_elements_both)):
            roi_n = repeated_elements_both[roi]
            f.write("{}".format(lines[roi_n-1]))
