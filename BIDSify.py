# For converting the output of dcm2niix into BIDS structure 
# Matches the output of Steiner MRI for TD study 

import os
import re 

def main(): 

    folder_prompt = "Are you in the folder with the MRI files? \n"
    BIDS_prompt = 'Have you converted the files to NIFTI format (with dcm2niix), and renamed them for BIDS (with "-b y")? \n'
    
    if not input(folder_prompt).__contains__("y"): 
        print("Move (cd) to the folder which contains the MRI data.")
        return 1 

    if not input(BIDS_prompt).__contains__("y"): 
        print(' Run this: dcm2niix -b y -z n -f "sub-[nn]_ses-1_series\%\s" -o [output folder] [DICOM folder] ')  
        return 2 

    datatypes = ["anat", "dwi", "fmap", "func", "perf", "anat/scout", "anat/DIS2D", "qsm", "spectroscopy"] 
    
    replacements = [
        None, 
        "scout", 
        "acq-sag_scout", 
        "acq-cor_scout", 
        "acq-tra_scout", 
        "T1w", 
        "acq-cor_T1w", 
        "acq-tra_T1w", 
        "DIS2D", 
        "T1w_another",  # What is series 9?  
        "Chimap", 
        "Chimap", 
        "spectroscopy-ACC", 
        "spectroscopy-ACC-ECC", 
        "spectroscopy-ACC-no-ECC", 
        "spectroscopy-RtStr", 
        "spectroscopy-RtStr-ECC", 
        "spectroscopy-RtStr-no-ECC",
        "asl_control" , # 18
        "asl_label", 
        "asl_difference", 
        "dir-PA_M0scan", 
        "dir-AP_M0scan", 
        "dir-PA_dwi", # 23 dti 
        "dir-AP_dwi", 
        "dir-PA_dwi_ADC", 
        "dir-PA_dwi_TRACEW", 
        "dir-PA_dwi_AF", 
        "dir-PA_dwi_tensor", 
        None, # Nothing in 29 
        "fieldmap", # 30 fmap
        "fieldmap", 
        "task-rest_bold", 
        "task-rest_bold_MoCo" 
    ]

    destinations = {
        "scout": "anat/scout", 
        "T1w": "anat", 
        "DIS2D": "anat/DIS2D",
        "Chimap": "qsm", 
        "spectroscopy": "spectroscopy", 
        "asl": "perf", 
        "M0": "perf", 
        "dwi": "dwi", 
        "fieldmap": "fmap", 
        # "gre-mt": "fmap", 
        "bold": "func"
    }

    # Create datatype folders (eg. anat/ ) 
    for datatype in datatypes: 
        try: 
            os.mkdir(datatype) 
        except: 
            print(f"The folder {datatype}/ already exists.")

    # Rename and move each file 
    files = os.listdir(os.curdir)
    for i in range(33, 0, -1):  
        look_for = "series" + str(i) 
        regex = re.compile(look_for)
        new_name = replacements[i] 
        # destination = destinations[new_code] # Which folder it will go into 
        new_home = ""
        for destination in destinations: 
            if destination in look_for: 
                new_home = destination 
                break 
        for file in files: 
            # m = regex.search(file)
            if look_for in file: 
            # if m:  
                fullname = regex.sub(new_name, file)
                os.rename(file, f"{destination}/{fullname}") 
    
    print("Success! There should now be a BIDS folder structure in this folder, with the files renamed.")
    return 0 

if __name__ == "__main__": 
    main()



""" replacements = {    
        # anat/  
        "T1_mprage_sag": "T1w", 
        # qsm/ 
        "QSM_3D_me_tra_e": "Chimap", 
        # dwi/ 
        "DTI_64_Dir": "dwi",  # DTI_64_Dir_APa , APb , and  PA 
        # fmap/ 
        "gre_field_map_e": "fieldmap", 
        # func/ 
        "BOLD_-_Resting_State": "bold", # BOLD_-_Resting_State  and  BOLD_-_Resting_State_MoCo 
        # perf/ 
        "fme_pcASL": "asl",  
        # scout/ 
        "AAHead_Scout_64ch-head-coil_i000": "scout-i", 
        "AAHead_Scout_64ch-head-coil": "scout", 
        # Unsure how to label -- not in BIDS specification 
        "2D_GRE_MT_tra_2mm": "gre-mt"
    }  """
