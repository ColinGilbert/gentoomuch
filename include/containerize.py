#!/usr/bin/env python3

import os, shutil, docker
from pathlib import Path
from .gentoomuch_common import output_path, image_tag_base
from .get_dockerized_profile_name import get_dockerized_profile_name
from .get_dockerized_stagedef_name import get_dockerized_stagedef_name
from .get_docker_tag import get_docker_tag
from .docker_stage_exists import docker_stage_exists
from .create_dockerfile import create_dockerfile
from .get_profiles import get_profiles
from .save_profiles import save_profiles
from .verify_tarball import verify_tarball

# This turns a tarball into a dockerized stage
def containerize(path : str, arch : str, profile : str, stage_define : str, upstream : bool) -> bool:
    print("CONTAINERIZING")
    if not verify_tarball(path):
        print("CONTAINERIZE: Could not verify tarball")
        return False
    # This tag is used to name an image that is imported as a bootstrap image.
    bootstrap_tag = image_tag_base + "bootstrap:latest"
    desired_tag = get_docker_tag(arch, profile, stage_define, upstream)
    temp_tag = get_docker_tag(arch, profile, stage_define, upstream, True)
    #print("Containerize... desired tag = " + desired_tag)
    # Which directory do we use to build?
    # If it exists, we're doing an update and thus we remove.
    bootstrap_dir = os.path.join(output_path, 'bootstrap')
    dockerfile = os.path.join(bootstrap_dir, 'Dockerfile')
    os.makedirs(bootstrap_dir, exist_ok = True)
    # Delete the dockerfile, if present from another build...
    if len(os.listdir(bootstrap_dir)) > 0:
        os.system('rm -rf ' + bootstrap_dir + '/*')
    tarball_name = os.path.split(path)[1]
    new_tarball_path = os.path.join(bootstrap_dir, tarball_name) 
    # Now create our dockerfile.
    if os.path.isfile(dockerfile):
        os.remove(dockerfile)
    with open(dockerfile, 'w') as file:
        file.write(create_dockerfile(tarball_name, profile))
    code = os.system('cp ' + path + ' ' +  new_tarball_path)
    if code != 0:
        print("Could not copy tarball from " + path + " to " + new_tarball_path)
        return False
    # We then import our bootstrap image, and build a new one using our dockerfile.
    # Then we get rid of the old bootstrap image.
    code = os.system("cd " + bootstrap_dir + " && docker import " + tarball_name  + " " + bootstrap_tag)
    if code != 0:
        print("Could not import tarball " + tarball_name)
        return False
    # TODO: Replace with renaming and allow recovery from backup.
    if docker_stage_exists(arch, profile, stage_define, upstream):
        code = os.system("docker rmi " + desired_tag)
        if code == 0:
            pass
    code = os.system("docker build -t " + desired_tag + " " + bootstrap_dir)
    if code != 0:   
        print("Could not docker-build")
        return False
    code = os.system("docker image rm -f " + bootstrap_tag + " &> /dev/null")
    if code != 0:
        print("Could not remove bootstrap image")
    #os.system('mv ' + new_tarball_path + ' ' + old_tarball_path)
    if code == 0:
        print("INFO: Succesfully dockerized " + desired_tag)
        profiles = set(get_profiles())
        if profile not in profiles:
            profiles.add(profile)
            save_profiles(profiles)
        return True
    else:
        return False
