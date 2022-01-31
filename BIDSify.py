import os
from posix import listdir 
import re 
from sys import path #, sys 

def main(): 

    folder_prompt = "Are you in the folder with the MRI files? \n"
    BIDS_prompt = 'Have you converted the files to NIFTI format (with dcm2niix), and renamed them for BIDS (with "-b y")? \n'
    
    if not input(folder_prompt).__contains__("y"): 
        print("Move (cd) to the folder which contains the MRI data.")
        return 1 

    if not input(BIDS_prompt).__contains__("y"): 
        print("Run this: [dcm2niix command TBC]") # TO DO  -- dcm2niix -b y -o sub-00x -f 
        return 2 

    # folder = os.path(sys.argv[1]) | os.curdir 
    folder = os.curdir 
    datatypes = ["anat", "dwi", "fmap", "func", "perf", "Dunno"] 
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
        # ??? Don't know what these are, so don't know which folder or label  
        "AAHead_Scout_64ch-head-coil_i000": "scout-i", 
        "AAHead_Scout_64ch-head-coil": "scout", 
        "2D_GRE_MT_tra_2mm": "gre-mt"
    } 
    destinations = {
        "T1": "anat", "Chimap": "anat", 
        "dwi": "dwi", "fieldmap": "fmap", 
        "bold": "func", "asl": "perf", 
        "scout-i": "Dunno", "scout": "Dunno", "gre-mt": "Dunno"
    }

    # Create datatype folders (eg. anat/ ) 
    for datatype in datatypes: 
        try: 
            os.mkdir(datatype) 
        except: 
            print(f"The folder {datatype}/ already exists.")

    print("\n\n\n")

    # Rename and move each file 
    files = os.listdir(folder)
    for old_code in replacements: 
        new_code = replacements[old_code] # Texts for replacing 
        regex = re.compile(old_code) 
        destination = destinations[new_code] # Which folder it will go into 
        for file in files: 
            if re.search(regex, file): 
                # new_name = path(file)
                # print(new_name)
                print(new_code)
                # os.rename(file, )
    

    return 0 

if __name__ == "__main__": 
    main()
        
        