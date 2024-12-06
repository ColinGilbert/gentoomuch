#!/usr/bin/env python3

# This sets the currently active basestage.
import os, sys, re, docker
from .gentoomuch_common import output_path, config_path, image_tag_base, active_image_tag, desired_packages_path, desired_hooks_path
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_dockerized_profile_name import get_dockerized_profile_name
from .portage_directory_combiner import portage_directory_combiner
from .get_docker_tag import get_docker_tag
from .composefile import create_composefile
from .write_file_lines import write_file_lines
from .patch_profile import patch_profile


def swap_stage(arch : str, profile : str, stage_def : str, upstream : bool, patch_to_test: str = ''):
    os.system('cd ' + output_path + ' && docker-compose down')
    # We assemble our (temporary) Portage directory from stages.
    combiner = portage_directory_combiner()
    combiner.process_stage_defines(stage_def)
    # We now add patches, per profile.
    patch_profile(arch, profile)
    dckr = docker.from_env()
    dckr_imgs = dckr.images.list()
    found = False
    t = get_docker_tag(arch, profile, stage_def, bool(upstream))
    print("TAG " + t)
    # print("ATTEMPTING TO SWAP: " + t)
    code = os.system('docker rmi ' + active_image_tag) # To ensure we don't suffer from duplicates.
    if code == 0:
        pass
    else:
        exit("Could not remove duplicate tag")
    for i in dckr_imgs:
        print(i)
        if t in i.tags:
            cmd = "docker image tag " + t + " " + active_image_tag
            code = os.system(cmd)
            if code == 0:
                pass
            else:
                exit("Cannot tag image " + t + "to " + i.tag)
            #i.tag(tag=active_image_tag) # We now actually tag the image we wanna use.
            found = True
            print('SWAPPED STAGE TO: ' + t)
            break
    if not found:
        sys.exit("FAILED TO SWAP STAGE: Could not find docker image " + t)
    if 'packages' in combiner.todo:
        if len(combiner.todo['packages']) > 0:
            write_file_lines(desired_packages_path, combiner.todo['packages'])
    if 'hooks' in combiner.todo:
        if len(combiner.todo['hooks']) > 0:
            write_file_lines(desired_hooks_path, combiner.todo['hooks'])
    create_composefile(output_path, patch_to_test)
    os.system('cd ' + output_path + ' && docker-compose up --no-start')
