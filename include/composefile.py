#!/usr/bin/env python3

import os, sys, re
from .gentoomuch_common import output_path, config_path, active_image_tag, stages_path, patches_workdir, patches_mountpoint, portage_output_path
from .write_file_lines import write_file_lines
from .get_active_stage import get_active_stage
from .tag_parser import tag_parser

builder_str = 'builder'
builder_privileged_str = builder_str + '-privileged'
updater_str = 'updater'
patcher_str = 'patcher'

containers = (builder_str, builder_privileged_str, updater_str, patcher_str)


# This uses the current state of the work/portage directory and automatically creates a composefile that'll properly include each file. This avoids much handcruft.
def create_composefile(output_path : str, exporting_patch : str = ''):
    lines = ['# Do not make changes to this file, as they will be overriden upon the next build.\n', 'services:\n']
    lines.extend(__output_config(builder_str))
    lines.extend(__output_config(builder_privileged_str))
    lines.extend(__output_config(updater_str))
    if exporting_patch != '':
        lines.extend(__output_config(patcher_str, exporting_patch))
    include_prefix = 'include/docker-compose/docker-compose.'
    lines.append('networks:\n')
    lines.append('  backend:\n')
    lines.append('    driver: bridge\n')
    lines.append('volumes:\n')
    lines.append('  distfiles:\n')
    lines.append('    driver: local\n')
    lines.append('  ebuilds:\n')
    lines.append('    driver: local\n')
    lines.append('  binpkgs:\n')
    lines.append('    driver: local\n')
    lines.append('  kernels:\n')
    lines.append('    driver: local\n')
    write_file_lines(os.path.join(output_path, 'docker-compose.yml'), lines)
    return True


def __output_config(container_type_str : str, exporting_patch : str = ''):
    if not container_type_str in containers:
        sys.exit('Gentoomuch.create-composefile: Invalid container type argument \"' + container_type_str  +  '\"')
    is_builder              = bool(container_type_str == builder_str)
    is_builder_privileged   = bool(container_type_str == builder_privileged_str)
    is_updater              = bool(container_type_str == updater_str)
    is_patcher              = bool(container_type_str == patcher_str)
    # Our results will be a list of strings.
    results = [] 
    # First, we define whether this'll be a builder or a packer.
    results.append('  gentoomuch-' + container_type_str + ':\n')
    # We append the universal parts.
    results.append('    # The following line is a cool trick that fools the docker program into using a locally-tagged image as if it came from a proper repository.\n')
    results.append('    image: ' + active_image_tag + '\n')
    results.append('    command: /bin/bash\n')
    results.append('    networks:\n')
    results.append('    - backend\n')
    results.append('    volumes:\n')
    results.append('    - /dev:/dev\n')
    results.append('    - /proc:/proc\n')
    results.append('    - /sys:/sys:ro\n')
    binpkg_str          = '    - binpkgs:/var/cache/binpkgs'
    distfiles_str       = '    - distfiles:/var/cache/distfiles'
    ebuilds_str         = '    - ebuilds:/var/db/repos/gentoo'
    kernels_str         = '    - kernels:/mnt/kernels'
    logs_mount_str      = '    - ./emerge.logs:/var/tmp/portage'
    results.append(binpkg_str + '\n')
    results.append(distfiles_str + '\n')
    results.append(ebuilds_str + '\n')
    results.append(kernels_str + '\n')
    results.append(logs_mount_str + '\n')
    # These are parts that have different permissions between the two types of containers.
    squashed_output_str = '    - ./squashed/blob:/mnt/squashed-portage'
    squashed_mount_str  = '    - ./squashed/mountpoint:/mnt/squashed-portage'
    stages_mount_str    = '    - ./stages:/mnt/stages'    
    # Here we actually write these differential parts into our list.
    if is_builder or is_builder_privileged or is_patcher:
        results.append(squashed_mount_str + '\n')
        results.append(stages_mount_str + '\n')
        results.append('    - ' + os.path.join('./patches.work', exporting_patch) + ':' + patches_mountpoint + '\n')
    if is_updater:
        results.append(squashed_output_str + '\n')
        results.append(stages_mount_str + ':ro\n')
    # Here we loop over the all the files in the portage directory and add them.
    for (dirpath, directories, files) in os.walk(portage_output_path):
        for f in files:
            if not f[0] == '.' and not f == 'README.md':
                rel_path = os.path.relpath(dirpath, output_path)
                results.append('    - ./' + os.path.join(rel_path, f) + ':' + os.path.join('/etc/', rel_path, f) + ':ro\n')
    if is_builder_privileged:
        results.append('    cap_add:\n')
        results.append('    - CAP_SYS_ADMIN\n')
        results.append('    - CAP_NET_ADMIN\n')
    # Finally, we return the list of string.
    return results
