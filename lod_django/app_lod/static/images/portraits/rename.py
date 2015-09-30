# http://stackoverflow.com/questions/2759067/rename-files-in-python
# Rename portraits : Singed_Square_0.png > Singed.png

import os
for filename in os.listdir("."):
    if filename.endswith(".png"):
        groups = filename.split('.')
        os.rename(filename, groups[0].capitalize() + '.png')