"""Read BrainVoyager VTC and export as NIfTI.

Designed for the 7 T motion quartet experiment data (2024).
"""

import os
import numpy as np
import bvbabel
import nibabel as nb
from pprint import pprint
from glob import glob

# =============================================================================
SUBJ = ['sub-01', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10']
MAIN_PATH = '/mnt/d/Exp-MotionQuartet/MRI_MQ/BOLD'
TASK = 'rest'
# =============================================================================

for su in SUBJ:
	
	PATH_VTC = os.path.join(MAIN_PATH, su, 'derivatives', 'func', 'sess-03', 'VTC_MNI')
	
	FILES = glob(os.path.join(PATH_VTC, "*{}*.vtc".format(TASK)))
	# print(FILES)

	OUTDIR = os.path.join(MAIN_PATH, su, 'derivatives', 'func', 'sess-03', 'NIFTI_MNI')
	# -----------------------------------------------------------------------------
	# Output directory
	if not os.path.exists(OUTDIR):
	    os.makedirs(OUTDIR)
	    print("  Output directory: {}\n".format(OUTDIR))

	# -----------------------------------------------------------------------------
	for f in FILES:
		# Load vtc
		if len(f) > 0:
			header, data = bvbabel.vtc.read_vtc(f, rearrange_data_axes=False)

			# See header information
			print('Converting VTC: {}'.format(f))

			# Transpose axes
			data = np.transpose(data, [0, 2, 1, 3])
			# Flip axes
			data = data[::-1, ::-1, ::-1, :]

			# Export nifti
			filename = os.path.basename(f)
			basename, ext = filename.split(os.extsep, 1)
			outname = os.path.join(OUTDIR, f"{basename}_bvbabel.nii.gz")
			img = nb.Nifti1Image(data, affine=np.eye(4))
			nb.save(img, outname)
		else:
			print('Time course does not exist')
		print("\n")

print("\nFinished.")
