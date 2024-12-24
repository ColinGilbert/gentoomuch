import os
from .gentoomuch_common import squashed_ports_filepath, user_scripts_path

# Cannot use "" in command
def exec_in_chroot(path: str, command: str):
    print("EXEC IN CHROOT - COMMAND: " + command)
    cmd_str = 'sudo mount -t proc /proc ' + os.path.join(path, 'proc') + ' && '
    cmd_str += 'sudo mount --rbind /dev ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo mount --make-rslave ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo mount --rbind /sys ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo mount --make-rslave ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo mount --rbind /tmp ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo mount --make-rslave ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo mount --bind /run ' + os.path.join(path, 'run') + ' && '
    cmd_str += 'sudo mkdir -p ' + os.path.join(path, 'var/db/repos/gentoo') + ' && '
    cmd_str += 'sudo mount -o loop,ro ' + squashed_ports_filepath + ' ' + os.path.join(path, 'var/db/repos/gentoo') + ' && '
    cmd_str += 'sudo mkdir -p ' + os.path.join(path,'mnt/user.scripts') + ' && '
    cmd_str += 'sudo mount --bind -o ro ' + user_scripts_path + ' ' + os.path.join(path,'mnt/user.scripts && ')
    cmd_str += 'sudo echo nameserver 8.8.8.8 > ' + os.path.join(path, 'etc', 'resolv.conf')
    code = os.system(cmd_str)
    if code != 0:
        print("COULD NOT MOUNT NECESSARY DIRS")
        return False

    cmd_str = 'sudo chroot ' + path + ' /bin/bash -c " . /etc/profile && '   + command + '"'
    user_execution_code = os.system(cmd_str)
    if user_execution_code == 0:
        pass
    
    cmd_str = 'sudo umount -fl ' + os.path.join(path, 'proc') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'run') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'var/db/repos/gentoo') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'mnt/user.scripts')
    code = os.system(cmd_str)
    if code == 0:
        pass
    else:
        print("ERROR UNMOUNTING DIRECTORIES")
        return False
    if user_execution_code != 0:
        return False
    return True