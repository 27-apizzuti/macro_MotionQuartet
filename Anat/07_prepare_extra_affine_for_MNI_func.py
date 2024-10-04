"""Prepare data for computing extra affine matrices for appling correctly MNI transformation"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from scipy import ndimage
import subprocess
from glob import glob

# Settings
STUDY_PATH = '/mnt/d/WB-MotionQuartet/derivatives'
SUB = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10',]

for su in SUB:
    print('Working on {}'.format(su))

    # // Load VMR
    FILE_VMR = glob(os.path.join(STUDY_PATH, su, 'anat', '00_preps_MNI', '*_acq-mp2rage_UNI_denoised_IIHC_ISOpt6.vmr'))[0]
    header_vmr, data_vmr = bvbabel.vmr.read_vmr(FILE_VMR)

    # Load VTC
    VTC_file = glob(os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '{}_task-rest_acq-2depimb4_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native.vtc'.format(su)))[0]
    header, tdata = bvbabel.vtc.read_vtc(VTC_file, rearrange_data_axes=False)
    print('Dimension of VTC {}'.format(np.shape(tdata)))
    data = tdata[..., 0:1]

    zoom_data = ndimage.zoom(data, (3, 3, 3, 1), order=0, output=np.float32)
    print('Size zoomed data: ', zoom_data.shape)

    nx = header["XEnd"] - header["XStart"]
    ny = header["YEnd"] - header["YStart"]
    nz = header["ZEnd"] - header["ZStart"]
    print('VTC size in VMR resolution: ', (nx, ny, nz))

    new_data = np.zeros(( data_vmr.shape + (data.shape[3],)), dtype=np.float32)

    new_data[header["ZStart"]-1:header["ZEnd"]-1,
    		header["YStart"]-1:header["YEnd"]-1,
    		 header["XStart"]-1:header["XEnd"]-1, :] = zoom_data

    # VTC -> NIFTI Transpose axes + Flip axes [512x 512x 512] at 0.6 iso mm
    new_data = np.transpose(new_data, [0, 2, 1, 3])
    new_data = new_data[::-1, ::-1, ::-1, :]
    basename = VTC_file.split(os.extsep, 1)[0]
    outname = "{}_short_bvbabel_resx3_float32.nii.gz".format(basename)
    img = nb.Nifti1Image(new_data, affine=np.eye(4))
    nb.save(img, outname)
    print("Finished.")

    # VTC -> NIFTI Transpose axes + Flip axes [x x ] at 1.8 iso mm
    data = np.transpose(data, [0, 2, 1, 3])
    data = data[::-1, ::-1, ::-1, :]
    data.astype(np.float32)
    print('Dimension of NIFTI at 1.8 {}'.format(np.shape(data)))
    basename = VTC_file.split(os.extsep, 1)[0]
    outname = "{}_short_bvbabel_resx1_float32.nii.gz".format(basename)
    temp = np.eye(4)
    temp[0, 0] *= 3.0
    temp[1, 1] *= 3.0
    temp[2, 2] *= 3.0
    temp[3, 3] *= 3.0

    img = nb.Nifti1Image(data, affine=temp)
    img.header["pixdim"][0] = 3  # mm
    img.header["pixdim"][1] = 3  # mm
    img.header["pixdim"][2] = 3  # mm
    nb.save(img, outname)
    print("Finished.")

    # VTC -> NIFTI entire time series
    tdata = np.transpose(tdata, [0, 2, 1, 3])
    tdata = tdata[::-1, ::-1, ::-1, :]
    tdata.astype(np.float32)
    print('Dimension of NIFTI at 1.8 {}'.format(np.shape(tdata)))
    basename = VTC_file.split(os.extsep, 1)[0]
    outname = "{}_bvbabel_resx1_float32.nii.gz".format(basename)
    temp = np.eye(4)
    temp[0, 0] *= 3.0
    temp[1, 1] *= 3.0
    temp[2, 2] *= 3.0
    temp[3, 3] *= 3.0

    img = nb.Nifti1Image(tdata, affine=temp)
    img.header["pixdim"][0] = 3  # mm
    img.header["pixdim"][1] = 3  # mm
    img.header["pixdim"][2] = 3  # mm
    nb.save(img, outname)
    print("Finished.")
