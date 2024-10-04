"""Exercise 1: GLMsingle
from: https://github.com/cvnlab/GLMsingle/blob/main/examples/example1.ipynb"""


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
from glmsingle.glmsingle import GLM_single
from bvbabel import vtc, sdm, vmp, prt
import pprint
import nibabel as nb
import time
# -----------------------------
def pad_volume(input_vol, outdims, xstart=0, ystart=0, zstart=0, xstop=-1, ystop=-1, zstop=-1):

    outvol = np.zeros(outdims)
    if len(input_vol.shape) == 4:
        outvol[xstart:,ystart:,zstart:zstop,:] = input_vol
    elif len(input_vol.shape) == 3:
        outvol[xstart:, ystart:, zstart:zstop] = input_vol

    return outvol

def save_to_vmp(vtc_hdr, map_names, data, outfile):

    temp_vmp_hdr, _ = vmp.create_vmp()
    temp_vmp_hdr['XStart'] = vtc_hdr['XStart']
    temp_vmp_hdr['XEnd'] = vtc_hdr['XEnd']
    temp_vmp_hdr['YStart'] = vtc_hdr['YStart']
    temp_vmp_hdr['YEnd'] = vtc_hdr['YEnd']
    temp_vmp_hdr['ZStart'] = vtc_hdr['ZStart']
    temp_vmp_hdr['ZEnd'] = vtc_hdr['ZEnd']
    temp_vmp_hdr['Resolution'] = 3
    temp_vmp_hdr['DimX'] = 512  # framing cube of the vmr
    temp_vmp_hdr['DimY'] = 512
    temp_vmp_hdr['DimZ'] = 512

    vmp_hdr = copy.deepcopy(temp_vmp_hdr)
    vmp_hdr['Map'][0]['MapName'] = map_names[0]
    vmp_hdr['Map'][0]['TypeOfMap'] = 15

    for name in map_names[1:]:

        temp = copy.deepcopy(temp_vmp_hdr)
        temp['Map'][0]['MapName'] = name
        temp['Map'][0]['TypeOfMap'] = 15
        vmp_hdr['Map'].extend(temp['Map'])

    vmp_hdr['NrOfSubMaps'] = int(len(map_names))
    vmp.write_vmp(outfile, vmp_hdr, data)

# ----- DATA FOLDER
# STUDY_PATH = "/home/ale/WB-MotionQuartet"
STUDY_PATH = "/mnt/d/WB-MotionQuartet"
SUBJ = ["sub-01", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]

# ------ Set parameters
N_TIME = 616
N_PREDICTORS = 2
TR = 1
STIM_DUR = 10
N_RUNS = 2

for su in SUBJ:
    print("###############################################################")
    print("Working on {}".format(su))

    VTC_PATH = os.path.join(STUDY_PATH, 'derivatives', su, 'func', "VTC_native".format(su))
    PROT_PATH = os.path.join(STUDY_PATH, 'Protocols', su, 'Exp1_Phys_MotQuart', 'Protocols')
    PATH_GLMSINGLE = os.path.join(STUDY_PATH, su, 'GLMsingle')
    os.makedirs(PATH_GLMSINGLE, exist_ok=True)

    opt = dict()                       # GLMsingle parameters
    opt['wantlibrary'] = 1
    opt['wantglmdenoise'] = 1
    opt['wantfracridge'] = 1
    opt['wantfileoutputs'] = [1,1,1,1]
    opt['wantmemoryoutputs'] = [1,1,1,1]

    # set number of cores to be used
    opt['n_jobs'] = 23
    # -------

    # CREATE DESIGN MATRIX
    design = []

    for it_run in range(0, N_RUNS):

        # // Load PRT
        hdr, prt_data = prt.read_prt(os.path.join(PROT_PATH, "Protocol_{}_Exp2_unamb_MotQuart_Run0{}.prt".format(su, it_run+1)))
        design_run = np.zeros([N_TIME, N_PREDICTORS])

        print('Add condition {}'.format(prt_data[1]['NameOfCondition']))    # Horizontal
        design_run[np.array(prt_data[1]['Time start']-1), 0] = 1

        print('Add condition {}'.format(prt_data[2]['NameOfCondition']))    # Vertical
        design_run[np.array(prt_data[2]['Time start']-1), 1] = 1

        # TRIM DESIGN MATRIX: Remove start and end fixation
        design_run_trim = design_run[20:596]

        print(design_run_trim[0:30])
        print(design_run_trim[550:])

        # // Append
        design.append(design_run_trim)

    print('Design matrix dims: {}'.format(np.shape(design)))

    # -------
    # CREATE DATA
    data = []

    for it_run in range(0, N_RUNS):

        # // Load VTC
        vtc_hdr, vtc_data =  vtc.read_vtc(os.path.join(VTC_PATH, "{}_task-phy_acq-2depimb4_run-0{}_SCSTBL_3DMCTS_bvbabel_undist_fix_BBR_native.vtc".format(su, it_run+1)))

        # TRIM VTC DATA
        vtc_data_trim = vtc_data[..., 20:596]
        data.append(vtc_data_trim)

    print('fMRI data dims: {}'.format(np.shape(data)))

    # -------
    t = time.time()

    # RUNNING GLMsingle
    glmsingle_obj = GLM_single(opt)

    # call GLMsingle (should take ~2 mins to run)
    results_glmsingle = glmsingle_obj.fit(
           design,
           data,
           STIM_DUR,
           TR,
           outputdir=PATH_GLMSINGLE,
           figuredir=os.path.join(PATH_GLMSINGLE, 'figures'))

    print(results_glmsingle.keys())

    elapsed = time.time() - t
    print(elapsed)

    # ------------------------
    # SAVE OUTPUT
    # // Save the noise predictors to sdm file
    for run in range(1,N_RUNS+1):

        # get nuisance regressors for model typec
        noise_regressors = results_glmsingle['typec']['pcregressors'][int(run)-1]
        hdr, sdm_data_temp = sdm.create_sdm()
        hdr['NrOfDataPoints'] = noise_regressors.shape[0]
        hdr['NrOfPredictors'] = noise_regressors.shape[1]

        sdm_data = []
        for i, noisets in enumerate(noise_regressors.T):
            temp = sdm_data_temp.copy()[0]
            temp['NameOfPredictor'] = 'NoiseRegressor' + str(i)
            temp['ValuesOfPredictor'] = noisets
            sdm_data.append(temp.copy())

        sdm.write_sdm(os.path.join(PATH_GLMSINGLE, "GLMdenoise_nuisance_regressors_run{run}.sdm".format(run)), hdr, sdm_data)

    # // Save noisepool volume
    noisepool_vol = results_glmsingle['typec']['noisepool'].astype(int)
    # add padding first on z axis
    noisepool_padded = pad_volume(noisepool_vol, vtc_data.shape[:3],zstart=30, zstop=71)
    save_to_vmp(vtc_hdr, ['noisepool'], noisepool_vol, PATH_GLMSINGLE + f'/GLMdenoise_noise_voxel_pool.vmp')

    # // save betas to vmp file
    # in this case add padding first on z axis
    # save betas for single-trials canonical HRF
    beta_fitHRF = results_glmsingle['typeb']['betasmd']
    # beta_fitHRF_padded = pad_volume(beta_fitHRF, vtc_data.shape[:3] + (beta_fitHRF.shape[-1],), zstart=30, zstop=71)
    beta_fitHRF_names = [f'betas_fitHRF_{trial_num + 1}' for trial_num in range(beta_fitHRF.shape[-1])]
    save_to_vmp(vtc_hdr, beta_fitHRF_names, beta_fitHRF, PATH_GLMSINGLE + '/betas_fitHRF.vmp')

    # save betas for single-trials fitted HRF
    beta_fitHRF_GLMdenoised = results_glmsingle['typec']['betasmd']
    beta_fitHRF_GLMdenoised_padded = pad_volume(beta_fitHRF_GLMdenoised, vtc_data.shape[:3] + (beta_fitHRF_GLMdenoised.shape[-1],), zstart=30, zstop=71)
    beta_fitHRF_names = [f'betas_fitHRF_GLMdenoise_{trial_num + 1}' for trial_num in
                         range(beta_fitHRF_GLMdenoised.shape[-1])]
    save_to_vmp(vtc_hdr, beta_fitHRF_names, beta_fitHRF_GLMdenoised, PATH_GLMSINGLE + '/betas_fitHRF_GLMdenoise.vmp')

    # save betas for single-trials fitted HRF regularised
    beta_fitHRF_GLMdenoised_RR = results_glmsingle['typed']['betasmd']
    beta_fitHRF_GLMdenoised_RR_padded = pad_volume(beta_fitHRF_GLMdenoised_RR, vtc_data.shape[:3] + (beta_fitHRF_GLMdenoised_RR.shape[-1],), zstart=30, zstop=71)
    beta_fitHRF_names = [f'betas_fitHRF_GLMdenoise_RR_{trial_num + 1}' for trial_num in
                         range(beta_fitHRF_GLMdenoised_RR.shape[-1])]
    save_to_vmp(vtc_hdr, beta_fitHRF_names, beta_fitHRF_GLMdenoised_RR, PATH_GLMSINGLE + '/betas_fitHRF_GLMdenoise_RR.vmp')
