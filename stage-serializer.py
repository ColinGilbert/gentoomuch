#!/usr/bin/env python3

# This saves out a named tarball of a given stage define.
import os, sys, re, shutil, docker
from include.gentoomuch_common import read_file_lines, write_file_lines, arch_config_path, current_basestage_path, includes_path, current_portage_path, stages_path, dockerfiles_path
from include.portage_directory_combiner import portage_directory_combiner

class stage_serializer:

    def __init__(self):
        self.dckr               = docker.from_env()
        self.tarballed          = False
        self.arch               = open(arch_config_path).read().strip()
        self.current_basestage  = open(current_basestage_path).read().strip()
        self.current_portage    = re.sub('/', '-', open(current_portage_path).read().strip())
        self.archive_name       = 'stage3-' + self.arch + '-' + self.current_basestage + '-' + self.current_portage
        self.extension          = '.tar'

    def save_stage(self):
        if os.path.isfile(arch_config_path) and os.path.isfile(current_basestage_path) and os.path.isfile(current_portage_path):
            needs_to_install_more_stuff = False
            packages = []
            archive_name = self.archive_name + self.extension 
            if os.path.isfile('./config/packages'):
                needs_to_install_more_stuff = True
                packages = read_file_lines('./config/packages')
            if os.path.isfile(os.path.join('./work/stages', archive_name)):
                os.remove(os.path.join('./work/stages', archive_name))
            packages_str = '&& emerge -K '
            for l in packages:
                packages_str += l.strip()
                packages_str += ' '
            # The following dogs' meal of a command preps a stage inside a docker container. It then changes root into it and emerges everything with -K. Then, it exists the chroot, unmounts all the chroot's temporary mounts, and creates from it a stage3 tarball under /mnt/stages/stage3-<arch>-<base>-xxxxx.tar.xz
            cmd_str = "docker-compose run gentoomuch-packer /bin/bash -c 'cd /mnt/gentoo && tar xpfv ../../stage3-*.tar.xz --xattrs-include=\'*.*\' --numeric-owner && mount -t proc none /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount -t tmpfs none /mnt/gentoo/tmp && mount -t tmpfs none /mnt/gentoo/var/tmp && rm -rf /mnt/gentoo/etc/portage/* && cp -R /etc/portage/* /mnt/gentoo/etc/portage && mount --bind /var/cache/binpkgs /mnt/gentoo/var/cache/binpkgs && mkdir /mnt/gentoo/var/db/repos/gentoo && mount --bind /var/db/repos/gentoo /mnt/gentoo/var/db/repos/gentoo && chroot . /bin/bash -c \"emerge -K --emptytree @world " + (packages_str if needs_to_install_more_stuff else "") + " &&  exit\" && umount -fl /mnt/gentoo/proc && umount -fl /mnt/gentoo/sys && umount -fl /mnt/gentoo/dev && umount -fl /mnt/gentoo/var/db/repos/gentoo && umount -fl /mnt/gentoo/var/cache/binpkgs && cd /mnt/gentoo && tar -cvf /mnt/stages/" + self.archive_name + self.extension + " . --xattrs --selinux --numeric-owner --acls && chown 1000:1000 /mnt/stages/" + self.archive_name + self.extension + "'"
            code = os.system(cmd_str)
            if code == 0:
                self.tarballed = True
        else:
            print('Could not open required config files.')
        return self.tarballed
    
def containerize(arch, basestage, portage):
    # TODO: Build from Dockerfile using self.dckr
    portage = re.sub('/', '-', portage)
    archive_name = 'stage3-' + arch + '-' + basestage + '-' + portage
    archive_ext = '.tar'
    os.system('cd ' + stages_path  + ' && docker import ' + archive_name + archive_ext + ' localhost:5000/gentoomuch-' + arch + '-' + basestage + '-' + portage + ':local ' )

#stage_serializer(True).save_stage()
#im_serial_guys = stage_serializer()
#im_serial_guys.save_stage()
containerize('amd64', 'default', 'gentoomuch-builder')
