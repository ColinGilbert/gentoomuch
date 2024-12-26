import os

def init():
    cmd_str = 'mkdir -p ~/gentoomuch-data & '
    cmd_str += 'mkdir -p ~/gentoomuch-data/{portage,stages,bootstrap,squashed_ports,squashed_ports_host_mountpoint} && '
    cmd_str += 'mkdir -p ~/gentoomuch-data/portage/{blob,mountpoint} && '
    cmd_str += 'touch ~/gentoomuch-data/profiles'# && '
    #cmd_str += "echo 'gentoo-sources' > ~/gentoomuch-data/kernel-sources"
    os.system(cmd_str)