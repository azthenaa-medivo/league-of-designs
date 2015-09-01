from fabric.api import run

def mm_on():
    run('mv maintenance-mode-off maintenance-mode-on')

def mm_off():
    run('mv maintenance-mode-on maintenance-mode-off')