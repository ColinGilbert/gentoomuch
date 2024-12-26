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
from .exec_user_hooks import exec_user_hooks

def save_tarball(arch: str, profile: str, stage_define: str, upstream: bool, patches: [str] = [], patches_have_been_compiled: bool = True, kconfig: str = '', friendly_name : str = '', custom_stage: str = '', scripts: [str] = [], removes: [str] = []):
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
    if upstream:
        swap_stage(arch, profile, stage_define = 'gentoomuch/builder', upstream = True)
    else:
        swap_stage(arch, profile, stage_define = 'gentoomuch/builder', upstream = False, custom_stage = custom_stage)
    packages = []
    if os.path.isfile(desired_packages_path):
        packages = read_file_lines(desired_packages_path)
    packages_str = ''
    for p in packages:
        packages_str += p.strip()
        if p.strip() != '':
            packages_str += ' '
    uid = get_gentoomuch_uid()
    gid = get_gentoomuch_gid()
    jobs = get_gentoomuch_jobs()
    print('PACKAGES TO INSTALL: ' + packages_str)
    if kconfig:
        print("KCONFIG: " + kconfig)
    cmd_str = "cd " + output_path + " && "
    cmd_str += "docker-compose run gentoomuch-builder /bin/bash -c \""
    cmd_str += "rm -rf /mnt/gentoo/* && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "tar xpf /stage3-* --numeric-owner && "
    cmd_str += "mkdir -p /mnt/gentoo/usr/src && "
    cmd_str += "rm -rf /mnt/gentoo/etc/portage/* && "
    cmd_str += "rsync -aXH /etc/portage/* /mnt/gentoo/etc/portage/ && "
    cmd_str += "chown -R root:root /mnt/gentoo/etc/portage/ && "
    cmd_str += "echo 'UTC' > /etc/timezone && "
    cmd_str += "echo 'nameserver 8.8.8.8' > /etc/resolv.conf && "
    if kconfig and not upstream:
        cmd_str += "cp " + os.path.join(kconfigs_mountpoint, kconfig + ".kconf") + " /usr/src/linux/.config && "
        cmd_str += "mkdir -p /mnt/gentoo/usr/src && "
        cmd_str += "ln -s /usr/src/linux /mnt/gentoo/usr/src/linux && "
        cmd_str += "echo 'MAKING " + kconfig + "' && "
        cmd_str += "cd /usr/src/linux && "
        cmd_str += "make -j" + jobs + " && "
        cmd_str += "INSTALL_PATH=/mnt/gentoo/boot make install && "
        cmd_str += "INSTALL_MOD_PATH=/mnt/gentoo make modules_install && "
        cmd_str += "touch /usr/src/linux/Module.symvers && " # Hack to compile zfs-kmod
    if upstream:
        cmd_str += "emerge --root=/ pigz && "
    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + (" --emptytree gentoo-sources " if upstream else " -uD --changed-use --newuse ") + packages_str + " @world && "
    cmd_str += "emerge --depclean --root=/mnt/gentoo --with-bdeps=n && "
    patch_counter = 0
    for patch in patches:
        if patch != '':
            patch_counter += 1
            valid, package = package_from_patch(patch, False)
            if valid:
                if patches_have_been_compiled:
                    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + " --oneshot =" + package + " && "
                else:
                    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + " --oneshot --onlydeps =" + package + " && "
                    cmd_str += "emerge --root=/mnt/gentoo -j" + jobs + " --oneshot --usepkg n =" + package + " && "
    if kconfig and not upstream:
        cmd_str += 'emerge --root=/mnt/gentoo --onlydeps @module-rebuild && '
        cmd_str += 'emerge --root=/mnt/gentoo --usepkg n @module-rebuild && '
    if patch_counter > 0:
        cmd_str += "emerge --depclean --root=/mnt/gentoo --with-bdeps=n && "
    if custom_stage != '':
        cmd_str += "emerge --root=/mnt/gentoo --unmerge @gentoomuch/builder && "
        if packages_str.strip() != '':
            cmd_str += "emerge --root=/mnt/gentoo " + packages_str + " && "    
        cmd_str += "emerge --depclean --root=/mnt/gentoo --with-bdeps=n && "
    cmd_str += "cd / && "
    cmd_str += "chown " + uid + ":" + gid + " -R /var/tmp/portage && "
    cmd_str += "cd /mnt/gentoo && "
    cmd_str += "echo 'SAVING STAGE INTO TAR ARCHIVE' && "
    cmd_str += "tar --exclude='./usr/src/*' --exclude='./dev/*' -cf /mnt/stages/" + archive_name + " . --use-compress-program=pigz --xattrs --selinux --numeric-owner --acls && "
    cmd_str += "chown " + uid + ":" + gid + " /mnt/stages/" + archive_name
    cmd_str += "\""
    code = os.system(cmd_str)
    if not code == 0:
        print("FAILED TO CREATE TARBALL: " + archive_name)
        return (False,'')
    results = sign_stage(path = os.path.join(stages_path, archive_name))
    if not results:
        print("COULD NOT SIGN STAGE")
        return (False, '')
    if len(scripts) > 0 or len(removes) > 0:
        results = exec_user_hooks(os.path.join(stages_path, archive_name), scripts, removes)
        if results == False:
            return (False,'')
    
    return (True, archive_name)
