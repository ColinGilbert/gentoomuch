#!/usr/bin/env python3

import os, sys
from .gentoomuch_common import output_path, config_path, active_image_tag, stages_path, patches_workdir, patches_export_mountpoint, portage_output_path, kernel_configs_path, kconfigs_mountpoint, kernels_out_path, squashed_ports_dir, squashed_ports_mountpoint
from .write_file_lines import write_file_lines
from .get_active_stage import get_active_stage
from .tag_parser import tag_parser

builder_str = 'builder'
updater_str = 'updater'
patcher_str = 'patcher'

containers = (builder_str, updater_str, patcher_str)

# This uses the current state of the work/portage directory and automatically creates a create_composefile that'll properly include each file. This avoids much handcruft.
def create_composefile(output_path : str, exporting_patch : str = ''):
    lines = ['# Do not make changes to this file, as they will be overriden upon the next build.\n', 'services:\n']
    lines.extend(__output_config(builder_str))
    lines.extend(__output_config(updater_str))
    lines.extend(__output_config(patcher_str, exporting_patch))
    include_prefix = 'include/docker-compose/docker-compose.'
    lines.append('networks:\n')
    lines.append('  backend:\n')
    lines.append('    driver: bridge\n')
    lines.append('volumes:\n')
    lines.append('  distfiles:\n')
    lines.append('    driver: local\n')
    lines.append('  repos:\n')
    lines.append('    driver: local\n')
    lines.append('  binpkgs:\n')
    lines.append('    driver: local\n')
    lines.append('  gentoo_root_tmp:\n')
    lines.append('    driver: local\n')
    lines.append('  kernel_src:\n')
    lines.append('    driver: local\n')
    write_file_lines(os.path.join(output_path, 'docker-compose.yml'), lines)
    return True

def __output_config(container_type_str : str, exporting_patch : str = ''):
    if not container_type_str in containers:
        sys.exit('Gentoomuch.create-create_composefile: Invalid container type argument \"' + container_type_str  +  '\"')
    is_builder              = bool(container_type_str == builder_str)
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
    results.append('    - binpkgs:/var/cache/binpkgs\n')
    results.append('    - distfiles:/var/cache/distfiles\n')
    results.append('    - repos:/var/db/repos\n')
    results.append('    - kernel_src:/usr/src\n')
    results.append('    - gentoo_root_tmp:/mnt/gentoo\n')
    results.append('    - ' + kernel_configs_path + ':' + kconfigs_mountpoint + '\n')
    # These are parts that have different permissions between the types of containers.
    stages_mount_str    = '    - ./stages:/mnt/stages'    
    # Here we write differentiated stuff into our list.
    if is_builder or is_patcher:
        results.append(stages_mount_str + '\n')
        if exporting_patch != '':
            results.append('    - ' + os.path.join('./patches.work', exporting_patch) + ':' + patches_export_mountpoint + '\n')
    if is_updater:
        results.append(stages_mount_str + ':ro\n')
        results.append('    - ' + squashed_ports_dir + ':' + squashed_ports_mountpoint + '\n')
    # Here we loop over the all the files in the portage directory and add them.
    for (dirpath, directories, files) in os.walk(portage_output_path):
        for f in files:
            if not f[0] == '.' and not f == 'README.md':
                rel_path = os.path.relpath(dirpath, output_path)
                results.append('    - ./' + os.path.join(rel_path, f) + ':' + os.path.join('/etc/', rel_path, f) + ':ro\n')
    # Finally, we return the list of string.
    return results
