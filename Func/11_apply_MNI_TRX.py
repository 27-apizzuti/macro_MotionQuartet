"""Apply MNI transformation"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from pprint import pprint
from scipy import ndimage
import subprocess
from glob import glob

SUB = ['sub-07']
STUDY_PATH = '/mnt/e/WB-MotionQuartet/derivatives'
TASK = ['amb']

myTarget = os.path.join(STUDY_PATH, 'MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISO1pt8_bvbabel.nii.gz')
myITK4 = os.path.join(STUDY_PATH, "anat_pt6_to_1pt8.txt")

mni_bbox = {'XStart': 108,
                'XEnd': 405,
                'YStart': 90,
                'YEnd': 471,
                'ZStart': 100,
                'ZEnd': 370}
for su in SUB:

    myITK1 = os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '{}_func1pt8_to_pt6.txt'.format(su))
    myITK2 = glob(os.path.join(STUDY_PATH, su, 'anat', '00_preps_MNI', 'ANTS', '*_MNI0GenericAffine.mat'))[0]
    myITK3 = glob(os.path.join(STUDY_PATH, su, 'anat', '00_preps_MNI', 'ANTS', '*_MNI1Warp.nii.gz'))[0]

    for ta in TASK:
        
        # nii_list = glob(os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '*_task-{}_acq-2depimb4_*_THPGLMF3c_BBR_native_bvbabel_resx1_float32.nii.gz'.format(ta)))
        nii_list = glob(os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '*_task-amb_acq-2depimb4_run-03_*THPGLMF3c_BBR_native_bvbabel_resx1_float32.nii.gz'))

        print(nii_list)

        for nii in nii_list:
            mysource = nii
            basename = nii.split(os.extsep, 1)[0]
            outname = "{}_bvbabel_resx1_float32_MNI.nii.gz".format(basename)
    

            print("Apply TRX on {}".format(mysource))
            command = f"antsApplyTransforms -d 3 -e 3 --float -i {mysource} -o {outname} -r {myTarget} -n LanczosWindowedSinc -t {myITK4} -t {myITK3} -t {myITK2} -t {myITK1}"
            subprocess.run(command, shell=True)

            print('Convert NIFTI MNI to VTC')
            NII_TO_VTC = outname
            datanii = nb.load(NII_TO_VTC).get_fdata()

            # Prepare nifti to create VTC
            # Transpose axes
            new_data = np.transpose(datanii, [0, 2, 1, 3])
            # Flip axes
            new_data = new_data[::-1, ::-1, ::-1, :]
            print(np.shape(new_data))
            
            VTC_file_REF = glob(os.path.join(STUDY_PATH, su, 'func', 'VTC_native', '*_task-{}_acq-2depimb4_run-01_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native.vtc'.format(ta)))[0]
            header, data = bvbabel.vtc.read_vtc(VTC_file_REF, rearrange_data_axes=False)
            
            pprint(header)
            
            header["XStart"] = mni_bbox["YStart"]
            header["XEnd"] = mni_bbox["YEnd"]
            
            header['YStart'] = mni_bbox["ZStart"]
            header['YEnd'] = mni_bbox["ZEnd"]
            
            header['ZStart'] = mni_bbox["XStart"]
            header['ZEnd'] = mni_bbox["XEnd"]
            header['Reference space (0:unknown, 1:native, 2:ACPC, 3:Tal, 4:MNI)'] = 4
            
            pprint(header)
            
            # Save VTC
            basename = NII_TO_VTC.split(os.extsep, 1)[0]
            outname = "{}.vtc".format(basename)
            bvbabel.vtc.write_vtc(outname, header, new_data, rearrange_data_axes=False)