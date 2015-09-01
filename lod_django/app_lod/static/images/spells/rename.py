__author__ = 'artemys'
# http://stackoverflow.com/questions/2759067/rename-files-in-python
# Remove _ from file names, so those that are Okay are Okay. See ?

import os
for filename in os.listdir("."):
    if filename.endswith(".png"):
        groups = filename.split('_')
        os.rename(filename, filename.replace('_',''))