import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import scipy
import scipy.io as sio
from os.path import join
import warnings
warnings.filterwarnings('ignore')
# from glmsingle.glmsingle import GLM_single
from bvbabel import vtc, sdm, vmp, prt
from pprint import pprint
import nibabel as nb


def save_to_nifti(nii_hdr, data, outname):

   img = nb.Nifti1Image(data, header=nii_hdr.header, affine=nii_hdr.affine)
   nb.save(img, outname)

# Load
design = np.load('D:\Git\macro_MotionQuartet\Func\modeling\GLMsingle_outputs\DESIGNINFO.npy',allow_pickle=True).item()
a = 5

#
#
#
#
#
# # Load nifti for header information
# FILE = "/mnt/d/temp-GLMsingle/VTC/sub-01_task-phy_acq-2depimb4_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_sess-03_BBR_slice44_bvbabel.nii.gz"
# nifti_file = nb.load(FILE)
#
#
# # load existing file outputs if they exist
# outputdir_glmsingle = '/mnt/d/temp-GLMsingle/GLMsingle_outputs_2preds'
# results_glmsingle = dict()
# results_glmsingle['typea'] = np.load(join(outputdir_glmsingle,'TYPEA_ONOFF.npy'),allow_pickle=True).item()
# results_glmsingle['typeb'] = np.load(join(outputdir_glmsingle,'TYPEB_FITHRF.npy'),allow_pickle=True).item()
# results_glmsingle['typec'] = np.load(join(outputdir_glmsingle,'TYPEC_FITHRF_GLMDENOISE.npy'),allow_pickle=True).item()
# results_glmsingle['typed'] = np.load(join(outputdir_glmsingle,'TYPED_FITHRF_GLMDENOISE_RR.npy'),allow_pickle=True).item()
#
# # ----- Betas ----
# # Save betas for each trials
# beta_fitHRF = results_glmsingle['typed']['betasmd']
# outputname = "/mnt/d/temp-GLMsingle/betasmd_typeD_trials.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# # ----- Average betas -----
#
# # Average betas
# beta_fitHRF = np.nanmean(results_glmsingle['typea']['betasmd'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/betasmd_typeA_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# # Average betas
# beta_fitHRF = np.nanmean(results_glmsingle['typeb']['betasmd'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/betasmd_typeB_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# beta_fitHRF = np.nanmean(results_glmsingle['typec']['betasmd'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/betasmd_typeC_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# beta_fitHRF = np.nanmean(results_glmsingle['typed']['betasmd'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/betasmd_typeD_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# # ------- R2 ------------
#
# # Average R2
# beta_fitHRF = np.nanmean(results_glmsingle['typeb']['R2'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/r2_typeB_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# beta_fitHRF = np.nanmean(results_glmsingle['typec']['R2'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/r2_typeC_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# beta_fitHRF = np.nanmean(results_glmsingle['typed']['R2'], axis=-1)
# outputname = "/mnt/d/temp-GLMsingle/r2_typeD_AVG.nii.gz"
# save_to_nifti(nifti_file, beta_fitHRF, outputname)
#
# # -----------------------
# # # save noisepool volume
# #  noisepool_vol = results_glmsingle['typec']['noisepool'].astype(int)
# #  # add padding first on z axis
# #  # noisepool_padded = pad_volume(noisepool_vol, vtc_data.shape[:3],zstart=30, zstop=71)
#
# #  save_to_vmp(vtc_hdr, ['noisepool'], noisepool_vol, PATH_GLMSINGLE + f'/GLMdenoise_noise_voxel_pool.vmp')
#
#
# #  # save betas to vmp file
# #  # in this case add padding first on z axis
# #  # save betas for single-trials canonical HRF
# #  beta_fitHRF = results_glmsingle['typeb']['betasmd']
# #  #beta_fitHRF_padded = pad_volume(beta_fitHRF, vtc_data.shape[:3] + (beta_fitHRF.shape[-1],), zstart=30, zstop=71)
# #  beta_fitHRF_names = [f'betas_fitHRF_{trial_num+1}' for trial_num in range(beta_fitHRF.shape[-1])]
#
# #  save_to_vmp(vtc_hdr, beta_fitHRF_names, beta_fitHRF,  PATH_GLMSINGLE + '/betas_fitHRF.vmp')
#
# #  # save betas for single-trials fitted HRF
# #  beta_fitHRF_GLMdenoised = results_glmsingle['typec']['betasmd']
# #  #beta_fitHRF_GLMdenoised_padded = pad_volume(beta_fitHRF_GLMdenoised, vtc_data.shape[:3] + (beta_fitHRF_GLMdenoised.shape[-1],), zstart=30, zstop=71)
# #  beta_fitHRF_names = [f'betas_fitHRF_GLMdenoise_{trial_num+1}' for trial_num in range(beta_fitHRF_GLMdenoised.shape[-1])]
# #  save_to_vmp(vtc_hdr, beta_fitHRF_names, beta_fitHRF_GLMdenoised,  PATH_GLMSINGLE + '/betas_fitHRF_GLMdenoise.vmp')
#
# #  # save betas for single-trials fitted HRF regularised
# #  beta_fitHRF_GLMdenoised_RR = results_glmsingle['typed']['betasmd']
# #  #beta_fitHRF_GLMdenoised_RR_padded = pad_volume(beta_fitHRF_GLMdenoised_RR, vtc_data.shape[:3] + (beta_fitHRF_GLMdenoised_RR.shape[-1],), zstart=30, zstop=71)
# #  beta_fitHRF_names = [f'betas_fitHRF_GLMdenoise_RR_{trial_num+1}' for trial_num in range(beta_fitHRF_GLMdenoised_RR.shape[-1])]
#  # save_to_vmp(vtc_hdr, beta_fitHRF_names, beta_fitHRF_GLMdenoised_RR,  PATH_GLMSINGLE + '/betas_fitHRF_GLMdenoise_RR.vmp')
#
