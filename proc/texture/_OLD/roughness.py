import os
import sys
sys.path.append(os.path.expanduser("~") + "/ivpy/src")
from ivpy import *
from ivpy.extract import extract
import pandas as pd

def get_image_list(indir,omit_folders=None):
    allfiles = []
    for root,dirs,files in os.walk(indir):
        for file in files:
            allfiles.append(root + "/" + file)

    if omit_folders is not None:
        if isinstance(omit_folders,list):
            for omit_folder in omit_folders:
                allfiles = [item for item in allfiles if omit_folder not in "".join(item.split("/")[:-1])]
        else:
            raise TypeError("'omit_folders' must be a list")

    return [item for item in allfiles if item[-4:]==".tif"]

def main():
    try:
        indir = sys.argv[1]
    except:
        raise TypeError("must supply a directory name")

    try:
        outfile = sys.argv[2]

        try:
            omit_folders = sys.argv[3:]
        except:
            omit_folders = None

    except:
        outfile = indir + "/" + indir.rstrip("/").split("/")[-1] + ".csv"

        try:
            omit_folders = sys.argv[2:]
        except:
            omit_folders = None

    image_list = get_image_list(indir,omit_folders)
    df = pd.DataFrame({"localpath":image_list})

    attach(df,"localpath")
    df["roughness"] = extract("roughness",verbose=True)
    df.to_csv(outfile,index=False)

if __name__ == "__main__":
    main()
