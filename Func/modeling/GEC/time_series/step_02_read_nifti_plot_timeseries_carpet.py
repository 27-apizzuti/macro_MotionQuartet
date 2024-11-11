"""Turn nifti timeseries with ROIs into carpet timeseries.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb
from glob import glob

# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
MAIN_PATH = '/mnt/e/WB-MotionQuartet/derivatives'

TASK = ['phy', 'rest']

# This affine gives starting indices at lower left hand corner in ITKSNAP
CUSTOM_AFFINE = np.array([[-1, 0, 0, 0],
		    			  [ 0, 1, 0, 0],
						  [ 0, 0, 1, 0],
				   		  [ 0, 0, 0, 1]])
# =============================================================================
for ta in TASK:
	for su in SUBJ:

		PATH_IN = os.path.join(MAIN_PATH, su, 'func', 'VTC_MNI')

		# Timecourses
		NII_TC = sorted(glob(os.path.join(PATH_IN, "{}_task-{}_run-0*_acq-2depimb4_SCSTBL_3DMCTS_bvbabel_undist_fix_THPGLMF3c_BBR_native_bvbabel_resx1_float32_bvbabel_resx1_float32_MNI.nii.gz".format(su, ta))))
		print(NII_TC)
		# Voxels of interest / regions of interest
		NII_VOI = os.path.join(MAIN_PATH, su, 'func', 'GEC', "Glasser_MNI_bilateral_NATIVE_VOIinVTCspace.nii.gz")


		OUTBASENAME = "{}".format(su)

		# -----------------------------------------------------------------------------
		# Figure out the necessary information
		# -----------------------------------------------------------------------------
		nr_runs = len(NII_TC)
		print(f"  Nr. runs {nr_runs}")

		# Load nifti time course
		nii_temp = nb.load(NII_TC[0])
		data_temp = np.asarray(nii_temp.dataobj)
		nr_timepoints = data_temp.shape[-1]
		print(f"  Nr. timepoints (per run) {nr_timepoints}")

		# Load nifti voxels on interest
		nii_voi = nb.load(NII_VOI)
		data_voi = np.asarray(nii_voi.dataobj)

		# Determine labels of ROI's
		labels = np.unique(data_voi)[1:]
		labels = labels.astype(int)
		nr_labels = labels.size
		print(f"  Nr. labels {nr_labels}")

		# -----------------------------------------------------------------------------
		# Fill in the carpet by looping over runs
		# -----------------------------------------------------------------------------
		carpet = np.zeros((nr_timepoints, nr_labels, nr_runs))
		carpet_vois = np.zeros((nr_timepoints, nr_labels, nr_runs ))
		carpet_runs = np.zeros((nr_timepoints, nr_labels, nr_runs))

		for n in range(nr_runs):

			if n > 0:  # First timeseries is already loaded before the loop
				nii_temp = nb.load(NII_TC[n])
				data_temp = np.asarray(nii_temp.dataobj)

			# Step 5: Pull out time courses
			for i in labels:
				# Pull out ROI data
				idx_roi = data_voi == i

				# Remove zeros if present
				temp = data_temp[idx_roi]
				idx_zeros = temp == 0

				# print('Number of nan: {}'.format(np.sum(np.isnan(temp))))
				# print('Number of zeros: {}'.format(np.sum(idx_zeros)))

				if np.sum(idx_zeros) > 0:
					temp[idx_zeros] = np.nan
					# print('Replacing zeros with NaN --> Number of nan: {}'.format(np.sum(np.isnan(temp))))
				# else:
				# 	print('No replaced')

				temp = np.nanmean(temp, axis=0)

				# Insert to carpet
				carpet[:, i-1, n] = temp
				carpet_vois[:, i-1, n] = i
				carpet_runs[:, i-1, n] = n+1

			print(f"  {n+1}/{nr_runs}")

		# -----------------------------------------------------------------------------
		# Unravel carpets
		# -----------------------------------------------------------------------------
		carpet = carpet.transpose([2, 0, 1])
		carpet_vois = carpet_vois.transpose([2, 0, 1])
		carpet_runs = carpet_runs.transpose([2, 0, 1])

		carpet = carpet.reshape([nr_runs*nr_timepoints, nr_labels])
		carpet_vois = carpet_vois.reshape([nr_runs*nr_timepoints, nr_labels])
		carpet_runs = carpet_runs.reshape([nr_runs*nr_timepoints, nr_labels])

		# Save
		# -----------------------------------------------------------------------------
		outname = os.path.join(PATH_IN, f"{OUTBASENAME}_{ta}_VOICarpet.nii.gz")
		img = nb.Nifti1Image(carpet, affine=CUSTOM_AFFINE)
		nb.save(img, outname)
		outname = os.path.join(PATH_IN, f"{OUTBASENAME}_{ta}_VOICarpet_labels-vois.nii.gz")
		img = nb.Nifti1Image(carpet_vois, affine=CUSTOM_AFFINE)
		nb.save(img, outname)
		outname = os.path.join(PATH_IN, f"{OUTBASENAME}_{ta}_VOICarpet_labels-runs.nii.gz")
		img = nb.Nifti1Image(carpet_runs, affine=CUSTOM_AFFINE)
		nb.save(img, outname)

print("\nFinished.")
