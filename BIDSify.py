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
        print("Run this: [dcm2niix command TBC]") # TO DO  -- dcm2niix -b y -o sub-00x -f 
        return 2 

    folder = os.curdir 
    datatypes = ["anat", "dwi", "fmap", "func", "perf"] 
    replacements = { 
        # anat/  
        "T1_mprage_sag": "T1", 
        "QSM_3D_me_tra_e": "Chimap", 
        # dwi/ 
        "DTI_64_Dir": "dwi",  # DTI_64_Dir_APa , APb , and  PA 
        # fmap/ 
        "gre_field_map_e": "fieldmap", 
        # func/ 
        "BOLD_-_Resting_State": "bold", # BOLD_-_Resting_State  and  BOLD_-_Resting_State_MoCo 
        # perf/ 
        "fme_pcASL": "asl",  
        # Unsure how to label these -- not in BIDS specification 
        "AAHead_Scout_64ch-head-coil_i000": "scout-i", 
        "AAHead_Scout_64ch-head-coil": "scout", 
        "2D_GRE_MT_tra_2mm": "gre-mt"
    } 
    destinations = {
        "T1": "anat", "Chimap": "anat", "scout-i": "anat", "scout": "anat", 
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

