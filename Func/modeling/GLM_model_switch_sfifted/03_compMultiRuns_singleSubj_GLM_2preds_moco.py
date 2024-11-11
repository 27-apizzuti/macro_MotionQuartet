"""
Compute multi-runs GLM

"""

import os
from glob import glob
print("Hello!")

# =============================================================================

STUDY_PATH = 'E:\\WB-MotionQuartet'
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
TASKS = ["amb"]

for su in SUBJ:
    print('Working on {}'.format(su))

    # // Testing batch script
    PATH_GLM = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'GLM_model2', 'MultiRuns_shifted')
    PATH_VTC = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'VTC_MNI')
    PATH_SDM = os.path.join(STUDY_PATH, 'derivatives', su, 'func', 'GLM_model2', 'SDM')

    if not os.path.exists(PATH_GLM):
        os.mkdir(PATH_GLM)

    for task in TASKS:
        print('Working on task {}'.format(task))
        VMR_MNI = os.path.join(STUDY_PATH, "derivatives", "MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr")
        doc = bv.open(VMR_MNI)
        doc.clear_multistudy_glm_definition()

        if task == 'phy':
            RUNS = ['1', '2']
        else:
            RUNS = ['1', '2', '3', '4']

        print('Creating .MDM considering {}'.format(len(RUNS)))

        for itrun in RUNS:
            vtc_file = os.path.join(PATH_VTC, '{}_task-{}_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc'.format(su, task, itrun))
            sdm = os.path.join(PATH_SDM, '{}_{}0{}_model2_shifted_MOCO.sdm'.format(su, task, itrun))
            doc.add_study_and_dm(vtc_file, sdm)

        doc.save_multistudy_glm_definition_file(os.path.join(PATH_GLM, '{}_{}_allRuns_shifted_MOCO.mdm'.format(su, task)))
        print('Running GLM for {}'.format(task))
        doc.serial_correlation_correction_level = 2 # 1 -> AR(1), 2 -> AR(2)
        doc.psc_transform_studies = True
        doc.z_transform_studies = False
        doc.z_transform_studies_baseline_only = False
        doc.separate_subject_predictors = False
        doc.separate_study_predictors = True
        doc.compute_multistudy_glm()
        doc.save_glm(os.path.join(PATH_GLM, '{}_{}_allRuns_MOCO_AR2_PSC_SSP_N-{}_shifted.glm'.format(su, task, len(RUNS))))
        doc.show_glm()
        doc.close()
