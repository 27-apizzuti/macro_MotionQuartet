"""Read BrainVoyager GLM and export Nifti."""

import os
import numpy as np
import nibabel as nb
import bvbabel
import pprint

STUDY_PATH = "/mnt/e/WB-MotionQuartet/derivatives"
SUBJ = ["sub-01", "sub-03", "sub-04","sub-05","sub-06","sub-07","sub-08","sub-09","sub-10"]

for su in SUBJ:
    FILES = [os.path.join(STUDY_PATH, su, 'func', 'GLM_model1', 'MultiRuns', "{}_amb_allRuns_MOCO_AR2_PSC_SSP_N-4.glm".format(su)),
    os.path.join(STUDY_PATH, su, 'func', 'GLM_model2', 'MultiRuns', "{}_amb_allRuns_MOCO_AR2_PSC_SSP_N-4.glm".format(su)),
    os.path.join(STUDY_PATH, su, 'func', 'GLM_model4', 'MultiRuns', "{}_amb_allRuns_MOCO_AR2_PSC_SSP_N-4.glm".format(su)),
    os.path.join(STUDY_PATH, su, 'func', 'GLM_model1', 'MultiRuns', "{}_phy_allRuns_MOCO_AR2_PSC_SSP_N-2.glm".format(su)),
    os.path.join(STUDY_PATH, su, 'func', 'GLM_model2', 'MultiRuns', "{}_phy_allRuns_MOCO_AR2_PSC_SSP_N-2.glm".format(su)),
    os.path.join(STUDY_PATH, su, 'func', 'GLM_model4', 'MultiRuns', "{}_phy_allRuns_MOCO_AR2_PSC_SSP_N-2.glm".format(su)),]

    for file in FILES:
        print(file)
        # =============================================================================
        # Load glm
        header, data_R2, data_SS, data_beta, data_SS_XiY, data_meantc, data_arlag = bvbabel.glm.read_glm(file)
        # See header information
        # pprint.pprint(header)
        # -----------------------------------------------------------------------------
        basename = file.split(os.extsep, 1)[0]

        # Multiple regression R value
        outname = "{}_R2_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(data_R2, affine=np.eye(4))
        nb.save(img, outname)

        # Sum of squares values
        outname = "{}_SS_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(data_SS.astype(np.int32), affine=np.eye(4))
        nb.save(img, outname)

        # Beta values
        outname = "{}_beta_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(data_beta, affine=np.eye(4))
        nb.save(img, outname)

        # Sum-of-squares indicating the covariation of each predictor with the time
        # course (SS_XiY). these values may be ignored for custom processing.
        outname = "{}_XY_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(data_SS_XiY, affine=np.eye(4))
        nb.save(img, outname)

        # Mean time course
        outname = "{}_meantc_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(data_meantc, affine=np.eye(4))
        nb.save(img, outname)

        # Auto-regression lag value
        outname = "{}_atrlag_bvbabel.nii.gz".format(basename)
        img = nb.Nifti1Image(data_arlag, affine=np.eye(4))
        nb.save(img, outname)

print("Finished.")
