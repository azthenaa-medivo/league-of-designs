import subprocess
import os
import argparse

if __name__ == '__main__':
    HERE = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='mode', nargs='?', help="'on' or 'off' or 'toggle', if not specified or broken will 'toggle'.", default='toggle')
    args = parser.parse_args()
    # Test if maintenance mode file is here
    if args.mode == 'on' or args.mode == '1':
        try:
            open(os.path.join(HERE, 'maintenance-mode-off'))
            # If we succeeded change the name.
            subprocess.call(['mv', os.path.join(HERE, 'maintenance-mode-off'), os.path.join(HERE, 'maintenance-mode-on')])
            print('Maintenance mode is now ON.')
        except IOError:
            print('Maintenance mode is already ON.')
    if args.mode == 'off' or args.mode == '0':
        try:
            open(os.path.join(HERE, 'maintenance-mode-on'))
            # If we succeeded change the name.
            subprocess.call(['mv', os.path.join(HERE, 'maintenance-mode-on'), os.path.join(HERE, 'maintenance-mode-off')])
            print('Maintenance mode is now OFF.')
        except IOError:
            print('Maintenance mode is already OFF.')
    if not args.mode or args.mode == 'toggle':
        try:
            open(os.path.join(HERE, 'maintenance-mode-on'))
            # If we succeeded change the name.
            subprocess.call(['mv', os.path.join(HERE, 'maintenance-mode-on'), os.path.join(HERE, 'maintenance-mode-off')])
            print('Maintenance mode is now OFF.')
        except IOError:
            subprocess.call(['mv', os.path.join(HERE, 'maintenance-mode-off'), os.path.join(HERE, 'maintenance-mode-on')])
            print('Maintenance mode is now ON.')