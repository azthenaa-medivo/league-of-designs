import os
import subprocess
from league_of_designs.settings import POSTIMPORT_PATH

def postimport(script, db="lod"):
    """Executes a Mongo map/reduce script from the sibling 'server/postimport' folder.

    Parameters:

    - script: script file name to execute.
    - db: database name (default to 'lod' for League of Designs)."""
    if os.path.isfile(os.path.join(POSTIMPORT_PATH, script)):
        subprocess.call(['mongo', db, os.path.join(POSTIMPORT_PATH, script)])

if __name__ == '__main__':
    print(SERVER_PATH)
    print(API_PATH)
    print(POSTIMPORT_PATH)
    print(os.path.isfile(os.path.join(POSTIMPORT_PATH, 'articles_postimport.js')))