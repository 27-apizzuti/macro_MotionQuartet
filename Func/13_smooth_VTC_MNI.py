import os
from glob import glob

STUDY_PATH = "E:\\WB-MotionQuartet\\derivatives"
SUBJ = ["sub-10"]

for su in SUBJ:
    VMR = os.path.join(STUDY_PATH, 'MNI_ICBM152_T1_NLIN_ASYM_09c_BRAIN_ISOpt6.vmr')
    PATH_VTC = os.path.join(STUDY_PATH, su, 'func', 'VTC_MNI')
    print('Working on {}'.format(su))
    vtc_files = glob(os.path.join(PATH_VTC, '{}_*.vtc'.format(su)))
    print('List of VTC: {}'.format(vtc_files))

    for vtc in vtc_files:

        #// Open VMR
        doc_vmr = bv.open(VMR)
        linked_VTC = doc_vmr.link_vtc(vtc)
        smoothed_VTC = doc_vmr.smooth_spatial(4, 'mm')
