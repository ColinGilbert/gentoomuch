#!/usr/bin/env python3

import os, sys, docker, re
from .gentoomuch_common import desired_packages_path, stages_path, output_path, kconfigs_mountpoint
from .read_file_lines import read_file_lines
from .write_file_lines import write_file_lines
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_docker_tag import get_docker_tag
from .swap_stage import swap_stage
from .get_local_stage3_name import get_local_stage3_name
from .get_local_stage4_name import get_local_stage4_name
from .containerize import containerize
from .get_gentoomuch_uid import get_gentoomuch_uid
from .get_gentoomuch_gid import get_gentoomuch_gid
from .get_gentoomuch_jobs import get_gentoomuch_jobs
from .package_from_patch import package_from_patch
from .build_kernel import build_kernel

def save_tarball(arch: str, profile: str, stage_define: str, upstream: bool, patches: [str] = [], patches_have_been_compiled: bool = True, kconfig: str = '', emerge_kernel: bool = False):
    # Important to swap our active stage first!
    if kconfig == '':
        archive_name = get_local_stage3_name(arch, profile, stage_define)
    else:
        archive_name = get_local_stage4_name(arch, profile, stage_define, kconfig)
    for patch in patches:
        if patch != '':
            valid, package = package_from_patch(patch, False)
            if not valid:
                print("SAVE TARBALL: Invalid patch name " + patch)
                return (False, '') 
    print("CREATING TARBALL: " + archive_name + " Using upstream image: " + str(upstream))
    if os.path.isfile(os.path.join(stages_path, archive_name)):
        os.remove(os.path.join(stages_path, archive_name))
    packages = []
    if os.path.isfile(desired_packages_path):
        packages = read_file_lines(desired_packages_path)
    packages_str = ''
    for p in packages:
        packages_str += p.strip()
        packages_str += ' '
    uid = get_gentoomuch_uid()
    gid = get_gentoomuch_gid()
    jobs = get_gentoomuch_jobs()
    print('PACKAGES TO INSTALL : ' + packages_str)
      # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges. Then, it exits the chroot, unmounts all temporaries, and packs a tarball as "stage3-<arch>-<base>-<user-stage-define>.tar.gz"
    cmd_str = "cd " + output_path + " && "
    cmd_str += "docker-compose run gentoomuch-builder-privileged /bin/bash -c \""
    cmd_str += "emerge pigz && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "mkdir -p /mnt/gentoo/etc/portage &&"
    cmd_str += "tar xpf /stage3-* --xattrs-include='*.*' --numeric-owner && "
    cmd_str += "rm -rf /mnt/gentoo/etc/portage/* && "
    cmd_str += "rsync -aXH /etc/portage/* /mnt/gentoo/etc/portage/ && "
    cmd_str += "mount -t proc none /mnt/gentoo/proc && "
    cmd_str += "mount -t tmpfs none /mnt/gentoo/tmp && "
    cmd_str += "mount --rbind /sys /mnt/gentoo/sys && "
    cmd_str += "mount --make-rslave /mnt/gentoo/sys && "
    #cmd_str += "mount -o bind /dev /mnt/gentoo/dev && "
    cmd_str += "mount --rbind /dev /mnt/gentoo/dev && "
    cmd_str += "mount --make-rslave /mnt/gentoo/dev && "
    cmd_str += "mount -t tmpfs none /mnt/gentoo/var/tmp && "
    cmd_str += "mkdir -p /mnt/gentoo/var/tmp/portage && "
    cmd_str += "mount --bind /var/tmp/portage /mnt/gentoo/var/tmp/portage && "
    cmd_str += "mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && "
    cmd_str += "mount --bind /usr/src /mnt/gentoo/usr/src && "
    #cmd_str += "mkdir -p /mnt/gentoo/mnt/ccache_portage && "
    #cmd_str += "mount --bind /mnt/ccache_portage /mnt/gentoo/mnt/ccache_portage && "
    cmd_str += "mkdir -p /mnt/gentoo/var/db/repos/gentoo && "
    cmd_str += "mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && "
    cmd_str += "mkdir -p /mnt/gentoo/mnt/kconfigs && "
    cmd_str += "mount --bind /mnt/kconfigs /mnt/gentoo/mnt/kconfigs && "
    cmd_str += "echo 'UTC' > ./etc/timezone && "
    cmd_str += "echo 'nameserver 8.8.8.8' > ./etc/resolv.conf && "
    cmd_str += "chroot . /bin/bash -c '" # Enter chroot
    cmd_str += "env-update && "
    cmd_str += ". /etc/profile && "
    cmd_str += "emerge --with-bdeps=y -j" + jobs + (" --emptytree " if upstream else " -uD --changed-use --newuse ") + packages_str + "@world && "
    for patch in patches:
        if patch != '':
            valid, package = package_from_patch(patch, False)
            if valid:
                if patches_have_been_compiled:
                    cmd_str += "emerge -j" + jobs + " --oneshot --oneshot =" + package + " && "
                else:
                    cmd_str += "emerge -j" + jobs + " --oneshot --onlydeps =" + package + " && "
                    cmd_str += "emerge -j" + jobs + " --oneshot --usepkg n =" + package + " && "
    if emerge_kernel:
        cmd_str += 'rm -rf /usr/src/* && '
        cmd_str += 'emerge sys-kernel/gentoo-sources && '
    if kconfig != '':
        cmd_str += "echo MAKING " + kconfig + " && "
        results = build_kernel(arch, profile, kconfig, jobs)
        if not results:
            print("COULD NOT BUILD KERNEL " + kconfig)
            return (False,'')
        cmd_str += "cd /usr/src/linux && "
        cmd_str += "make install && "
        cmd_str += "make modules_install && "
        cmd_str += 'emerge --onlydeps @module-rebuild && '
        cmd_str += 'emerge --usepkg n @module-rebuild && '
        cmd_str += "rm certs/signing_key.pem & "
        cmd_str += "rm certs/signing_key.x509 & "
    #cmd_str += "emerge --depclean --with-bdeps=n && " # Remove build deps
    cmd_str += "cd / && "
    cmd_str += "chown " + uid + ":" + gid + " -R /var/tmp/portage "
    cmd_str += "' && " # Exit chroot
    cmd_str += "umount -fl /mnt/gentoo/tmp && "
    cmd_str += "umount -fl /mnt/gentoo/proc && "
    cmd_str += "umount -fl /mnt/gentoo/sys && "
    cmd_str += "umount -fl /mnt/gentoo/dev && "
    cmd_str += "umount -fl /mnt/gentoo/var/db/repos/gentoo && "
    cmd_str += "umount -fl /mnt/gentoo/var/cache/binpkgs && "
    cmd_str += "umount -fl /mnt/gentoo/var/tmp/portage && "
    cmd_str += "umount -fl /mnt/gentoo/usr/src && "
    cmd_str += "umount -fl /mnt/gentoo/mnt/kconfigs && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "echo 'SAVING STAGE INTO TAR ARCHIVE' && "
    cmd_str += "tar -cf /mnt/stages/" + archive_name + " . --use-compress-program=pigz --xattrs --selinux --numeric-owner --acls && "
    cmd_str += "chown " + uid + ":" + gid + " /mnt/stages/" + archive_name
    cmd_str += "\""
    swap_stage(arch, profile, stage_define, upstream)
    code = os.system(cmd_str)
    if not code == 0:
        print("FAILED TO CREATE TARBALL: " + archive_name)
        return (False,'')
    return (True, archive_name)
