import subprocess
import os

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    open(os.path.join(HERE, 'maintenance-mode-on'))
    # If we succeeded change the name.
    subprocess.call(['mv', os.path.join(HERE, 'maintenance-mode-on'), os.path.join(HERE, 'maintenance-mode-off')])
    print('Maintenance mode is now OFF.')
except IOError:
    subprocess.call(['mv', os.path.join(HERE, 'maintenance-mode-off'), os.path.join(HERE, 'maintenance-mode-on')])
    print('Maintenance mode is now ON.')