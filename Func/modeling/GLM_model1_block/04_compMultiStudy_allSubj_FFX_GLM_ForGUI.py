"""
Compute multi-study GLM FFX

@author: apizz

"""

import os
from glob import glob
print("Hello!")

# =============================================================================

STUDY_PATH = 'E:\\WB-MotionQuartet\\derivatives'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
TASKS = ['phy', 'amb']
PATH_GLM = os.path.join(STUDY_PATH, 'GLM_model1')
os.makedirs(PATH_GLM, exist_ok=True)

for task in TASKS:
    # // Open VMR
    VMR_MNI = os.path.join(STUDY_PATH, "MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr")
    print(VMR_MNI)
    doc = bv.open(VMR_MNI)
    doc.clear_multistudy_glm_definition()
    print('Creating .MDM for {}'.format(task))

    if task == 'phy':
        RUNS = ['1', '2']
    else:
        RUNS = ['1', '2', '3', '4']

    for su in SUBJ:
        print('Adding VTC and SDM from {}'.format(su))
        # // Adding single subject DMs
        PATH_VTC = os.path.join(STUDY_PATH, su, 'func', 'VTC_MNI')
        PATH_SDM = os.path.join(STUDY_PATH, su, 'func', 'GLM_model1', 'SDM')
        if not os.path.exists(PATH_GLM):
            os.mkdir(PATH_GLM)

        for itrun in RUNS:
            vtc_file = os.path.join(PATH_VTC, '{}_task-{}_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc'.format(su, task, itrun))
            sdm = os.path.join(PATH_SDM, '{}_{}0{}_2preds_MOCO.sdm'.format(su, task, itrun))
            doc.add_study_and_dm(vtc_file, sdm)

    doc.serial_correlation_correction_level = 2 # 1 -> AR(1), 2 -> AR(2)
    doc.psc_transform_studies = True
    doc.z_transform_studies = False
    doc.z_transform_studies_baseline_only = False
    doc.separate_subject_predictors = True
    doc.separate_study_predictors = False
    doc.save_multistudy_glm_definition_file(os.path.join(PATH_GLM, 'AllSbj_{}_2preds_MOCO_PSC_SEPSTUDYPREDS_N-{}_FFX.mdm'.format(task, len(SUBJ))))

    print('Save MDM')
#doc.compute_rfx_glm()
#doc.load_multistudy_glm_definition_file(os.path.join(PATH_GLM, 'AllSbj_ses-02_dir-AP_task-memories_EMem_Param-allPreds_N-{}.mdm'.format(len(SUBJ))))

#doc.compute_multistudy_glm()
#doc.save_glm(os.path.join(PATH_GLM, 'AllSbj_ses-02_dir-AP_task-memories_EMem_Param-allPreds_AR2_PSC_FFX_N-{}_withSMOOTH.glm'.format(len(SUBJ))))
#doc.show_glm()
#doc.close()
