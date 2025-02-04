"""Turn PRT files into labels for fMRI carpet timeseries.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import nibabel as nb
import bvbabel
from glob import glob
# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
MAIN_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
TR_in_ms = 1000
TASK = 'amb'

# This affine gives starting indices at lower left hand corner in ITKSNAP
CUSTOM_AFFINE = np.array([[-1, 0, 0, 0],
		    			  [ 0, 1, 0, 0],
						  [ 0, 0, 1, 0],
				   		  [ 0, 0, 0, 1]])

# =============================================================================
for su in SUBJ:
	
	# BrainVoyager stimulation protocol files
	PRTS = []
	
	if TASK == 'amb':
		PRTS_FILES = [glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/Protocols/sess-03/Exp1_Amb_MotQuart/Protocols/Protocol_{}_Protocols_sess-03_*.prt".format(su, su))]
	else:
		PRTS_FILES = [glob("/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD/{}/Protocols/sess-03/Exp1_Phys_MotQuart/Protocols/Protocol_{}_Exp2_unamb_MotQuart_Run*.prt".format(su, su))]

	for it in PRTS_FILES:
		for t in it:
			PRTS.append(t)

	# Reference carpet timecourse
	NII_TC = os.path.join(MAIN_PATH, su, 'derivatives', 'func', 'sess-03', 'NIFTI_MNI', '{}_{}_VOICarpet.nii.gz'.format(su, TASK))
	PATH_IN = os.path.join(MAIN_PATH, su, 'derivatives', 'func', 'sess-03', 'NIFTI_MNI')
	OUTBASENAME = "{}".format(su)

	# -----------------------------------------------------------------------------
	# Determine necessary information
	# -----------------------------------------------------------------------------
	nr_runs = len(PRTS)
	print(f"  Nr. runs {nr_runs}")

	nii1 = nb.load(NII_TC)
	data1 = np.asarray(nii1.dataobj)

	nr_timepoints = data1.shape[0] // nr_runs
	nr_voxels = data1.shape[1]
	print(f"  Nr. timepoints {nr_timepoints}")
	print(f"  Nr. voxels {nr_voxels}")


	carpet_prt = np.zeros((nr_timepoints, nr_voxels, nr_runs))

	# -----------------------------------------------------------------------------
	# Read PRT and put it into 2D nifti format
	# -----------------------------------------------------------------------------
	for n in range(nr_runs):
		header_prt, data_prt = bvbabel.prt.read_prt(PRTS[n])

		# Print header information
		print("\nPRT header")
		for key, value in header_prt.items():
		    print("  ", key, ":", value)

		# Print data
		print("\nPRT data")
		for d in data_prt:
		    for key, value in d.items():
		        print("  ", key, ":", value)
		    print("")

		# Convert PRT to nifti


		if TASK == 'amb':
			for i in range(int(header_prt["NrOfConditions"])):

				print(data_prt[i]["NameOfCondition"])
				if data_prt[i]["NameOfCondition"] == 'Horizontal':
					label = 1
				elif data_prt[i]["NameOfCondition"] == 'Vertical':
					label = 1
				elif data_prt[i]["NameOfCondition"] == 'Baseline':
					label = 2
				elif data_prt[i]["NameOfCondition"] == 'Nuisance':
					label = 3
				else:
					label = 0
				
				for ii in range(int(data_prt[i]["NrOfOccurances"])):
					j = round(float(data_prt[i]["Time start"][ii]) / TR_in_ms);
					k = round(float(data_prt[i]["Time stop"][ii]) / TR_in_ms);
					carpet_prt[j:k, :, n] = label
		else:
			for i in range(int(header_prt["NrOfConditions"])):


				if data_prt[i]["NameOfCondition"] == 'Horizontal':
					label = 1
				elif data_prt[i]["NameOfCondition"] == 'Vertical':
					label = 1
				elif data_prt[i]["NameOfCondition"] == 'Baseline':
					label = 2
				elif data_prt[i]["NameOfCondition"] == 'Nuisance':
					label = 3
				else:
					label = 0
				
				for ii in range(int(data_prt[i]["NrOfOccurances"])):
					j = data_prt[i]["Time start"][ii]-1;
					k = data_prt[i]["Time stop"][ii];
					carpet_prt[j:k, :, n] = label		

	# Unravel
	carpet_prt = carpet_prt.transpose([2, 0, 1])
	carpet_prt = carpet_prt.reshape([nr_runs*nr_timepoints, nr_voxels])

	# Save
	outname = os.path.join(PATH_IN, f"{OUTBASENAME}_{TASK}_VOICarpet_PRT_MotFlick.nii.gz")
	img = nb.Nifti1Image(carpet_prt, affine=CUSTOM_AFFINE)
	nb.save(img, outname)

print("\nFinished.")
