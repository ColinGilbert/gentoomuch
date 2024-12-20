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
from .sign_stage import sign_stage

def save_tarball(arch: str, profile: str, stage_define: str, upstream: bool, patches: [str] = [], patches_have_been_compiled: bool = True, kconfig: str = '', strip_deps: bool = False, friendly_name : str = '', custom_stage: str = ''):
    if friendly_name != '':
        archive_name = friendly_name + ".tar.gz"
    else:
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
    if kconfig:
        print("KCONFIG: " + kconfig)
    cmd_str = "cd " + output_path + " && "
    cmd_str += "docker-compose run gentoomuch-builder /bin/bash -c \""
    cmd_str += "rm -rf /mnt/gentoo/* && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "tar xpf /stage3-* --numeric-owner && "
    # cmd_str += "mkdir -p /usr/src/linux && "
    cmd_str += "mkdir -p /mnt/gentoo/usr/src && "
    cmd_str += "rm -rf /mnt/gentoo/etc/portage/* && "
    cmd_str += "rsync -aXH /etc/portage/* /mnt/gentoo/etc/portage/ && "
    cmd_str += "echo 'UTC' > /etc/timezone && "
    cmd_str += "echo 'nameserver 8.8.8.8' > /etc/resolv.conf && "
    if not upstream:
        cmd_str += "ln -s /usr/src /mnt/gentoo/usr/src && "
    if upstream:
        cmd_str += "emerge --root=/ pigz && "
    cmd_str += "emerge --with-bdeps=y --root=/mnt/gentoo -j" + jobs + (" --emptytree gentoo-sources " if upstream else " -uD --changed-use --newuse ") + packages_str + " @world && "
    for patch in patches:
        if patch != '':
            valid, package = package_from_patch(patch, False)
            if valid:
                if patches_have_been_compiled:
                    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + " --oneshot --oneshot =" + package + " && "
                else:
                    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + " --oneshot --onlydeps =" + package + " && "
                    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + " --oneshot --usepkg n =" + package + " && "
    if kconfig:
        cmd_str += "echo 'MAKING " + kconfig + "' && "
        cmd_str += "cp " + os.path.join(kconfigs_mountpoint, kconfig + ".kconf") + " /usr/src/linux/.config && "
        cmd_str += "cd /usr/src/linux && "
        cmd_str += "make -j" + jobs + " && "
        cmd_str += "INSTALL_PATH=/mnt/gentoo/boot make install && "
        cmd_str += "INSTALL_MOD_PATH=/mnt/gentoo make modules_install && "
        cmd_str += 'emerge --onlydeps --root=/mnt/gentoo @module-rebuild && '
        cmd_str += 'emerge --usepkg n --root=/mnt/gentoo @module-rebuild && '
    if custom_stage != '':
        cmd_str += "emerge --root=/mnt/gentoo --unmerge @gentoomuch/builder && "
        cmd_str += "emerge --root=/mnt/gentoo " + packages_str + " && "
    if strip_deps:
        cmd_str += "emerge --depclean --root=/mnt/gentoo --with-bdeps=n && "
    cmd_str += "cd / && "
    cmd_str += "chown " + uid + ":" + gid + " -R /var/tmp/portage && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "echo 'SAVING STAGE INTO TAR ARCHIVE' && "
    cmd_str += "tar --exclude='./usr/src' -cf /mnt/stages/" + archive_name + " . --use-compress-program=pigz --xattrs --selinux --numeric-owner --acls  && "
    cmd_str += "chown " + uid + ":" + gid + " /mnt/stages/" + archive_name
    cmd_str += "\""
    if upstream:
        swap_stage(arch, profile, stage_define =  'gentoomuch/builder', upstream = True)
    else:
        swap_stage(arch, profile, stage_define = 'gentoomuch/builder', upstream = False, custom_stage = custom_stage)
    code = os.system(cmd_str)
    if not code == 0:
        print("FAILED TO CREATE TARBALL: " + archive_name)
        return (False,'')
    print("SIGNING STAGE " + archive_name)
    sign_stage(path = os.path.join(stages_path, archive_name))
    return (True, archive_name)
