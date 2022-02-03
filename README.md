# bidsify
automatically converting our MRI data into BIDS format 

We get MRI data from a Siemens MAGNETOM Prisma. We convert the DICOM output to NIfTI using `dcm2niix`. This script will rename and rearrange the files to match the BIDS specification. 

Thanks to https://github.com/bids-standard/bids-validator
