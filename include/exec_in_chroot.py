import os

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
    cmd_str += 'sudo chroot ' + path + ' /bin/bash -c " . /etc/profile && '   + command + '" && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'proc') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'dev') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'sys') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'tmp') + ' && '
    cmd_str += 'sudo umount -fl ' + os.path.join(path, 'run')
    code = os.system(cmd_str)
    if code != 0:
        return False
    return True