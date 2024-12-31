import os

def init():
    cmd_str = 'mkdir -p ~/gentoomuch-data & '
    cmd_str += 'mkdir -p ~/gentoomuch-data/portage && '
    cmd_str += 'mkdir -p ~/gentoomuch-data/stages && '
    cmd_str += 'mkdir -p ~/gentoomuch-data/bootstrap && '
    cmd_str += 'mkdir -p ~/gentoomuch-data/squashed_ports && '
    cmd_str += 'mkdir -p ~/gentoomuch-data/squashed_ports_host_mountpoint'
    #cmd_str += "echo 'gentoo-sources' > ~/gentoomuch-data/kernel-sources"
    os.system(cmd_str)