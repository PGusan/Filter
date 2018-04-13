from tkinter.filedialog import askdirectory
from tkinter import *
from pathlib import Path
import os.path
root = Tk()
root.withdraw()

root_folder = str(askdirectory(title='Choose the Depot folder'))
cfiles_set = set()
include_path_set = set()
mak_files_set = set()

mak_file_path = Path(root_folder, "make\\Build\\Makefile.project.part.defines")
outputfile_path = os.path.join(os.getcwd(), r'makefile_outputfiles')
# Set path to the files based on root folder

try:
    with open(mak_file_path) as make_file:
        for line in make_file:
            if "APP_SOURCE_LST" in line:
                match_file = re.search("([^ ]+\.c\s)", line)
                if match_file:
                    match_file = match_file.group(1)
                    cfiles_set.add(match_file)

            if "ADDITIONAL_INCLUDES" in line:
                match_include_file = line.rsplit(' ', 1)[1]
                if match_include_file:
                    if "$(GENDATA_DIR)" in match_include_file:
                        match_include_file = match_include_file.replace("$(GENDATA_DIR)", "..\..\Vector_GenData")
                    include_path_set.add(match_include_file)
            match_mak_files = re.search("([^ ]+\.mak\s)", line)
            if match_mak_files:
                match_mak_files = match_mak_files.group(1)
                if "$(RTE_MAKEFILE_DIR)" in match_mak_files:
                    match_mak_files = match_mak_files.replace("$(RTE_MAKEFILE_DIR)", "..\..\Vector_GenData\mak")
                mak_files_set.add(match_mak_files)

    outputfile = open(outputfile_path + ".txt", "w", encoding="utf-8")
    outputfile.write("*****************************************************" + "\n")
    outputfile.write("C files" + "\n")
    outputfile.write("*****************************************************" + "\n")
    for cfile in cfiles_set:
        outputfile.write(''.join(str(item) for item in cfile))

    outputfile.write("*****************************************************" + "\n")
    outputfile.write("Included files Paths" + "\n")
    outputfile.write("*****************************************************" + "\n")

    for includefile in include_path_set:
        outputfile.write(''.join(str(item) for item in includefile))

    outputfile.write("*****************************************************" + "\n")
    outputfile.write("Mak Files found" + "\n")
    outputfile.write("*****************************************************" + "\n")

    for makfiles in mak_files_set:
        outputfile.write(''.join(str(item) for item in makfiles))
        mak_path_tmp = makfiles.rsplit("\\..\\")[1]
        mak_path_tmp = Path(root_folder, mak_path_tmp)
        mak_path_tmp = str(mak_path_tmp).strip()
        if os.path.exists(mak_path_tmp):
            print("path exists")
        else:
            print("no file")
    outputfile.close()
except OSError as e:
    print(e)
