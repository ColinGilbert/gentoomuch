import os
from .gentoomuch_common import squashed_ports_filepath

# Cannot use "" in command
def exec_in_chroot(path: str, command: str):
    cmd_str = 'sudo mount -t proc /proc ' + os.path.join(path, 'proc') + ' && '
    cmd_str += 'sudo mount --rbind /dev ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo mount --make-rslave ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo mount --rbind /sys ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo mount --make-rslave ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo mount --rbind /tmp ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo mount --make-rslave ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo mount --bind /run ' + os.path.join(path, 'run') + ' && '
    cmd_str += 'sudo mkdir -p ' + os.path.join(path, 'var/db/repos/gentoo') + ' && '
    cmd_str += 'sudo mount -o loop ' + squashed_ports_filepath + ' ' + os.path.join(path, 'var/db/repos/gentoo') + ' && '
    cmd_str += 'sudo echo nameserver 8.8.8.8 > ' + os.path.join(path, 'etc', 'resolv.conf') + ' && '
    cmd_str += 'sudo chroot ' + path + ' /bin/bash -c " . /etc/profile && '   + command + '"'

    user_execution_code = os.system(cmd_str)
    
    cmd_str = 'sudo umount -fl ' + os.path.join(path, 'proc') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'var/db/repos/gentoo') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'run')
    code = os.system(cmd_str)
    if code == 0:
        pass

    if user_execution_code != 0:
        return False
    return True