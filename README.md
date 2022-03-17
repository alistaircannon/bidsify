# bidsify
automatically converting our MRI data into BIDS format 

We get MRI data from a Siemens MAGNETOM Prisma. We convert the DICOM output to NIfTI using `dcm2niix`. This script will rename and rearrange the files to match the BIDS specification. 

Thanks to https://github.com/bids-standard/bids-validator

Our data:- 

```
sub-0x/ 
	anat/ 
		T1 (T1_mprage_sag) 
		Chimap = QSM (QSM_3D_me_tra_e)  
		scout (AAHead_Scout_64ch-head-coil) 
	dwi/ 
		dwi = DTI (DTI_64_Dir_)
	fmap/ 
		fieldmap (gre_field_map) 
		gre-mt (2D_GRE_MT_tra_2mm) 
	func/ 
		bold (BOLD_-_Resting_State) 
	perf/ 		
		asl (fme_pcASL) 

``` 

The BIDS specification does not list "scout" and "gre" as valid modality suffixes. 

		
		
