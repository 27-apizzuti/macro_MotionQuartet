"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
import scipy.stats

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
THRESHOLD = 4
TASKS = ['phy', 'amb']
VOLUME = 10

for it, task_type in enumerate(TASKS):

    print('Working on {}'.format(task_type))
    DIC_NAME = os.path.join(STUDY_PATH, 'GroupStat', 'AllSbj_{}_task_conjunction_models_thre_{}_dictionaryROI_{}_vox_COVERAGE.npz'.format(task_type, THRESHOLD, VOLUME))

    # Load the .npz file
    mydict = np.load(DIC_NAME)

    # Access arrays in the loaded dictionary
    print('There are {} ROIs preferring model1 '.format(len(mydict['Model1_pref'])))
    print('There are {} ROIs preferring model2 '.format(len(mydict['Model2_pref'])))
    print('There are {} ROIs preferring both '.format(len(mydict['Both_pref'])))

    # Open Glasser names
    with open("/mnt/e/WB-MotionQuartet/derivatives/GLM_model1/RFX_wSMOOTH/bilateral_Glasser_MNI_labels.txt", 'r') as f:
        lines = f.readlines()

    # Output file
    basename = DIC_NAME.split(os.extsep, 1)[0]
    res_txt = "{}_NAMES_COVERAGE.txt".format(basename)

    # print('For physical, I am writing ROI: {} with {} voxels'.format(roi_n, mydict['Phy_pref_count'][roi]))
    with open(res_txt, 'w') as f:
        f.write("Model 1.\n")
        for roi in range(0, len(mydict['Model1_pref'])):
            roi_n = mydict['Model1_pref'][roi]
            f.write("{}, {}\n".format(lines[roi_n-1].strip(), str(mydict['Model1_pref_count'][roi])))

        f.write("\nModel 2.\n")
        for roi in range(0, len(mydict['Model2_pref'])):
            roi_n = mydict['Model2_pref'][roi]
            f.write("{}, {}\n".format(lines[roi_n-1].strip(), str(mydict['Model2_pref_count'][roi])))

        f.write("\nBoth.\n")
        for roi in range(0, len(mydict['Both_pref'])):
            roi_n = mydict['Both_pref'][roi]
            f.write("{}, {}\n".format(lines[roi_n-1].strip(), str(mydict['Both_pref_count'][roi])))

    # Only save bilateral activation
    temp = mydict['Model2_pref']

    idx = temp > 180
    temp[idx] = temp[idx] - 180
    unique, counts = np.unique(temp, return_counts=True)
    repeated_elements_model2 = unique[counts > 1]

    temp = mydict['Model1_pref']
    idx = temp > 180
    temp[idx] = temp[idx] - 180
    unique, counts = np.unique(temp, return_counts=True)
    repeated_elements_model1 = unique[counts > 1]

    temp_both = mydict['Both_pref']
    idx = temp_both > 180
    temp_both[idx] = temp_both[idx] - 180
    unique, counts = np.unique(temp_both, return_counts=True)
    repeated_elements_both = unique[counts > 1]

    res_txt = "{}_NAMES_BILATERAL_COVERAGE.txt".format(basename)
    with open(res_txt, 'w') as f:
        f.write("Model 1.\n")
        for roi in range(0, len(repeated_elements_model1)):
            roi_n = repeated_elements_model1[roi]
            f.write("{}".format(lines[roi_n-1]))
        f.write("\nModel 2.\n")
        for roi in range(0, len(repeated_elements_model2)):
            roi_n = repeated_elements_model2[roi]
            f.write("{}".format(lines[roi_n-1]))
        f.write("\nBoth.\n")
        for roi in range(0, len(repeated_elements_both)):
            roi_n = repeated_elements_both[roi]
            f.write("{}".format(lines[roi_n-1]))
