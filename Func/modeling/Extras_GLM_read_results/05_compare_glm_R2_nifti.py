"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ["sub-01", "sub-03", "sub-04","sub-05","sub-06","sub-07","sub-08","sub-09","sub-10"]

TASK = ['phy', 'amb']

for ta in TASK:

    avg_diff = np.zeros([99, 127,90])
    avg_model1 = np.zeros([99, 127,90])
    avg_model2 = np.zeros([99, 127,90])
    avg_model_values = np.zeros([99, 127,90])


    for su in SUBJ:

        VMP_REF =  os.path.join(STUDY_PATH, 'sub-01', 'func', 'GLM_model1', 'MultiRuns', 'sub-01_amb_model1.vmp')
        header, data = bvbabel.vmp.read_vmp(VMP_REF)

        if ta == 'amb':
            model1 =os.path.join(STUDY_PATH, su, 'func', 'GLM_model1', 'MultiRuns', '{}_amb_allRuns_MOCO_AR2_PSC_SSP_N-4_R2_bvbabel.nii.gz'.format(su))
            model2 =os.path.join(STUDY_PATH, su, 'func', 'GLM_model2', 'MultiRuns', '{}_amb_allRuns_MOCO_AR2_PSC_SSP_N-4_R2_bvbabel.nii.gz'.format(su))
        else:
            model1 =os.path.join(STUDY_PATH, su, 'func', 'GLM_model1', 'MultiRuns', '{}_phy_allRuns_MOCO_AR2_PSC_SSP_N-2_R2_bvbabel.nii.gz'.format(su))
            model2 =os.path.join(STUDY_PATH, su, 'func', 'GLM_model2', 'MultiRuns', '{}_phy_allRuns_MOCO_AR2_PSC_SSP_N-2_R2_bvbabel.nii.gz'.format(su))

        # Load model 1
        nii = nb.load(model1)
        niidata = np.asarray(nii.dataobj)
        # Load model 2
        nii2 = nb.load(model2)
        niidata2 = np.asarray(nii2.dataobj)

        # Compute the difference
        diff = niidata - niidata2
        outname = os.path.join(STUDY_PATH, su, 'func',  '{}_{}_allRuns_R2diffmodel1_minus_model2_bvbabel.nii.gz'.format(su, ta))
        img = nb.Nifti1Image(diff, header=nii.header, affine=nii.affine)
        nb.save(img, outname)

        # Write VMP
        basename = outname.split(os.extsep, 1)[0]
        outname = "{}_bvbabel.vmp".format(basename)
        bvbabel.vmp.write_vmp(outname, header, diff)

        # Accumulate values across Subjects
        avg_diff = avg_diff + diff
        avg_model1 = avg_model1 + niidata
        avg_model2 = avg_model2 + niidata2

    # Copute the average
    avg_model1 = avg_model1 / len(SUBJ)
    avg_model2 = avg_model2 / len(SUBJ)
    avg_diff = avg_diff / len(SUBJ)

    # Find positive and negative
    idx1 = avg_diff > 0
    idx2 = avg_diff < 0
    avg_model_values[idx1] = avg_model1[idx1]
    avg_model_values[idx2] = avg_model2[idx2]
    avg_model_values[np.abs(avg_model_values) < 0.2] = 0

    # Adapt header
    header2 = header
    header2['Map'][0]['UpperThreshold'] = 0.1
    header2['Map'][0]['MapThreshold'] = 0
    header2['Map'][0]['MapName'] = 'R2 differences (+ model1, -model2)'

    outname = os.path.join(STUDY_PATH,  'AllSubj_{}_allRuns_R2diffmodel1_minus_model2_bvbabel.vmp'.format(ta))
    bvbabel.vmp.write_vmp(outname, header2, diff)

    # Adapt header
    header3 = header
    header3['Map'][0]['UpperThreshold'] = 0.7
    header3['Map'][0]['MapThreshold'] = 0
    header3['Map'][0]['MapName'] = 'R2 of winning'

    outname = os.path.join(STUDY_PATH,  'AllSubj_{}_allRuns_R2diffmodel1_minus_model2_values_bvbabel.vmp'.format(ta))
    bvbabel.vmp.write_vmp(outname, header3, avg_model_values)

print("Finished.")
