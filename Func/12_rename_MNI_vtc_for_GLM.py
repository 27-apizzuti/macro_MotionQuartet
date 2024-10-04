import os
from glob import glob
import shutil

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']

for su in SUBJ:
    print('Working on {}'.format(su))

    PATH_VTC = os.path.join(STUDY_PATH, su, 'func', 'VTC_MNI')
    VTC_LIST = glob(os.path.join(PATH_VTC, '*.vtc'))
    
    print(VTC_LIST)

    for vtc_name in VTC_LIST:

        basename = vtc_name.split("/")[-1]
        filename = basename.split("_")
        new_name = filename[0] + '_' + filename[1] + '_' + filename[3] + '_' + filename[2] + '_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.vtc'  
        vtc_file_out = os.path.join(PATH_VTC, new_name)
        print(vtc_file_out)
      
        # put run number first for a correct modelling
        shutil.move(vtc_name, vtc_file_out)
