#!/usr/bin/env python3

import os, sys
from .munging import read_file_lines, write_file_lines

builder_str = 'builder'
packer_str = 'packer'
updater_str = 'updater'

# This uses the current state of the work/portage directory and automatically creates a composefile that'll properly include each file. This avoids much handcruft.
def create_composefile():
    lines = ['# Do not make changes to this file, as they will be overriden upon the next build.\n' , 'services:\n']
    lines.extend(output_config(builder_str))
    lines.extend(output_config(packer_str))
    lines.extend(output_config(updater_str))
    include_prefix = 'include/docker-compose/docker-compose.'
    lines.extend(read_file_lines(include_prefix + 'tail'))
    return lines


def output_config(container_type_str):
    if not container_type_str == builder_str and not container_type_str == packer_str and not container_type_str == updater_str:
        sys.exit('Gentoomuch.create-composefile: Invalid container type argument \"' + updater_str  +  '\"')
    is_builder  = bool(container_type_str == builder_str)
    is_packer   = bool(container_type_str == packer_str)
    is_updater  = bool(container_type_str == updater_str)
    # Our results will be a list of strings.
    results = [] 
    # First, we define whether this'll be a builder or a packer.
    results.append('  gentoomuch-' + container_type_str + ':\n')
    # We append the universal parts.
    results.append('    # The following line is a cool trick that fools the docker program into using a locally-tagged image as if it came from a proper repository. As you can infer, our own scripts tag the current stage as "gentoomuch-stage3"')
    results.append('    image: localhost:5000/gentoomuch-stage3\n')
    results.append('    networks:\n')
    results.append('    - backend\n')
    results.append('    tmpfs:\n')
    results.append('    - /var/tmp\n')
    results.append('    - /tmp\n')
    results.append('    - /mnt/temp\n')
    results.append('    volumes:\n')
    results.append('    - /dev:/dev\n')
    results.append('    - /proc:/proc\n')
    results.append('    - /sys:/sys:ro\n')
    # These are the parts that have different permissions between the two types of containers.
    binpkg_str          = '    - binpkgs:/var/cache/binpkgs'
    distfiles_str       = '    - distfiles:/var/cache/distfiles'
    ebuilds_str         = '    - ebuilds:/var/db/repos/gentoo'
    stages_str          = '    - stages:/mnt/stages'
    kernels_str         = '    - kernels:/mnt/kernels'
    squashed_output_str = '    - ./work/squashed/squashed-portage:/mnt/squashed-portage'
    squashed_mount_str  = '    - ./work/squashed/squashed-portage/mountpoint:/mnt/squashed-portage'
    # Here we actually write these differential parts into our list.
    if is_packer:
        results.append(binpkg_str + ':ro\n')
        results.append(distfiles_str + ':ro\n')
        results.append(ebuilds_str + ':ro\n')
        results.append(stages_str + '\n')
        results.append(kernels_str + ':ro\n')
        results.append(squashed_mount_str + ':ro\n')
    if is_builder:
        results.append(binpkg_str + '\n')
        results.append(distfiles_str +'\n')
        results.append(ebuilds_str + '\n')
        results.append(stages_str + ':ro\n')
        results.append(kernels_str + '\n')
        results.append(squashed_mount_str + ':ro\n')
    if is_updater:
        results.append(binpkg_str + '\n')
        results.append(distfiles_str +'\n')
        results.append(ebuilds_str + '\n')
        results.append(stages_str + ':ro\n')
        results.append(kernels_str + '\n')
        results.append(squashed_output_str + '\n')
    # Here we loop over the all the files in the config/portage directory and add them.
    portage_cfg = './work/portage/'
    portage_tgt = '/etc/portage/'
    files = [f for f in os.listdir(portage_cfg) if os.path.isfile(os.path.join(portage_cfg, f))]
    for f in files:
        if f != '.gitignore':
            results.append('    - ' + portage_cfg + f + ':' + portage_tgt + f + ':ro\n')
    # We also do the same for the directories.
    dirs = [dr for dr in os.listdir(portage_cfg) if os.path.isdir(os.path.join(portage_cfg, f))]
    for d in dirs:
        if d != '.git':
            results.append('    - ' + portage_cfg + d + ':' + portage_tgt + d + ':ro\n')
    # Finally, we return the list of string.
    return results

  
def
