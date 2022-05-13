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
        print("Run this: [dcm2niix command TBC]") # TO DO  -- dcm2niix -b y -o sub-0x -f 
        return 2 

    folder = os.curdir 
    datatypes = ["anat", "dwi", "fmap", "func", "perf", "anat/scout", "anat/DIS2D", "qsm"] 
    replacements = { 
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
    } 
    replacements = 

    destinations = {
        "T1w": "anat", 
        "Chimap": "qsm", 
        "scout-i": "anat/scout", 
        "scout": "anat/scout", 
        "DIS2D": "anat/DIS2D"
        "dwi": "dwi", 
        "fieldmap": "fmap", "gre-mt": "fmap", 
        "bold": "func", 
        "asl": "perf"
        
    }

    # Create datatype folders (eg. anat/ ) 
    for datatype in datatypes: 
        try: 
            os.mkdir(datatype) 
        except: 
            print(f"The folder {datatype}/ already exists.")

    # Rename and move each file 
    files = os.listdir(folder)
    for old_code in replacements: 
        new_code = replacements[old_code] # Texts for replacing 
        regex = re.compile(old_code) 
        destination = destinations[new_code] # Which folder it will go into 
        for file in files: 
            m = regex.search(file)
            if m:  
                new_name = regex.sub(new_code, file)
                os.rename(file, f"{destination}/{new_name}") 

    print("Success! There should now be a BIDS folder structure in this folder, with the files renamed.")
    return 0 

if __name__ == "__main__": 
    main()

