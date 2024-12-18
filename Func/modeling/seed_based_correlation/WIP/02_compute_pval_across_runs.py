import numpy as np
import nibabel as nb
from statsmodels.stats.multitest import multipletests
import os
from scipy import stats

# // Setting input FILES
STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
LAGS = [1,-1, 0, 2,-2, 3,-3]      # seconds
TASKS = ['amb', 'phy', 'rest']
PATH_OUT =  "/mnt/e/WB-MotionQuartet/derivatives/GroupStat/SEED_CORR_SWITCH"

# Add brainmask
BRAINMASK = "/mnt/e/WB-MotionQuartet/derivatives/MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel_brainmask.nii.gz"
nii =  nb.load(BRAINMASK)
data = np.asarray(nii.dataobj)
idx_mask = data > 0

for task in TASKS:

    if task == 'amb':
        RUNS = [1, 2, 3, 4]
    if task == 'phy':
        RUNS = [1, 2]
    if task == 'rest':
        RUNS = [1]

    for lag in LAGS:
        print('Computing average for {} {}'.format(task, lag))
        avg_corr_sbj = np.zeros([99, 127, 90, len(SUBJ)])
        pval_corr_sbj = np.zeros([99, 127, 90, len(SUBJ)])
        thr_pval_corr_sbj = np.zeros([99, 127, 90, len(SUBJ)])

        for itsu, su in enumerate(SUBJ):

            PATH_IN = os.path.join(STUDY_PATH, su, 'func', 'SEED_CORR_SWITCH')
            avg_corr = np.zeros([99, 127, 90])
            avg_pval = np.zeros([99, 127, 90])
# ------------------------------------------------------------------------------
            for run in RUNS:
                FILE_CORR = '{}_task-{}_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI_seed_corr_{}.nii.gz'.format(su, task, run, lag)
                FILE_PVAL = '{}_task-{}_run-0{}_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI_seed_corr_{}_pval.nii.gz'.format(su, task, run, lag)

                # Load correlation nifti
                nii =  nb.load(os.path.join(PATH_IN, FILE_CORR))
                seed_corr = np.asarray(nii.dataobj)
                avg_corr = avg_corr + seed_corr

                # Load p-values nifti
                img =  nb.load(os.path.join(PATH_IN, FILE_PVAL))
                p_value_map = img.get_fdata()
                avg_pval = avg_pval + p_value_map

            # // Average correlation maps
            avg_corr = avg_corr / len(RUNS)

            # // Compute average p-value
            avg_pval = avg_pval / len(RUNS)
            idx_not_nan = (avg_pval > 0) | (avg_pval == 0)
            idx = idx_not_nan* idx_mask

            # Apply FDR correction
            temp_avg_pval_mask = avg_pval[idx]
            significant_mask_flat, adjusted_p_values_flat, _, _ = multipletests(temp_avg_pval_mask, alpha=0.05, method='fdr_bh')

            # Append single-subject result
            avg_corr_sbj[..., itsu] = avg_corr
            thr_pval_corr_sbj[idx, itsu] = significant_mask_flat
            pval_corr_sbj[idx, itsu] = adjusted_p_values_flat

        # // Save ALL SUBJECTS
        outname_CORR = os.path.join(PATH_OUT, 'AllSbj_task-{}_MNI_seed_corr_avg_{}_CORR_brainmask.nii.gz'.format(task, lag))
        img = nb.Nifti1Image(avg_corr_sbj, affine=nii.affine, header=nii.header)
        nb.save(img, outname_CORR)

        outname_PVAL = os.path.join(PATH_OUT, 'AllSbj_task-{}_MNI_seed_corr_avg_{}_PVAL_brainmask.nii.gz'.format(task, lag))
        img = nb.Nifti1Image(pval_corr_sbj, affine=nii.affine, header=nii.header)
        nb.save(img, outname_PVAL)

        outname_PVAL = os.path.join(PATH_OUT, 'AllSbj_task-{}_MNI_seed_corr_avg_{}_PVAL_THR_brainmask.nii.gz'.format(task, lag))

        img = nb.Nifti1Image(thr_pval_corr_sbj, affine=nii.affine, header=nii.header)
        nb.save(img, outname_PVAL)

print("Finished.")
