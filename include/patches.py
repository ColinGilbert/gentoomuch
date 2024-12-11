#!/usr/bin/env python3

import os, re, shutil, git
from .gentoomuch_common import output_path, portage_output_path, saved_patches_path, patches_workdir, patches_export_mountpoint
from .get_gentoomuch_uid import get_gentoomuch_uid
from .get_arch import get_arch
from .swap_stage import swap_stage
from .get_desired_profile import get_desired_profile
from .composefile import create_composefile
from .package_from_patch import package_from_patch
from .apply_saved_patches import apply_saved_patches

def get_first_commit(repo_path : str) -> str:
    return "git -C " + repo_path + " log | grep commit | tail -2 | head -1 | sed -e 's/commit //g' "


def validate_package_format(package : str) -> bool:
    if len(package.split('/')) < 2:
        print("setup_patch(): package name needs to be fully qualified. Got: " + package)
        return False
    return True


def get_patches_in_progress():
    if not os.path.isdir(patches_workdir):
        os.makedirs(patches_workdir, exist_ok = True)
    for root, dirs,files in os.walk(patches_wprldir):
        for f in files:
            print(f)


def send_diff(path_from: str, path_to : str, patch_name : str) -> bool:
    valid, versioned_package = package_from_patch(patch_name)
    if not valid == True:
        print("Send diff: Could not derive package name") 
        return False
    print("Send diff: " + versioned_package)
    base_path = os.path.join(path_from, patch_name, versioned_package)
    for d in os.listdir(base_path):
        print(d)
    final_path = os.path.join(base_path, d)
    print("PATCH PATH: " + final_path)
    repo = git.Repo(final_path)
    # Get first commit.
    first_commit = list(repo.iter_commits('master'))[-1]
    num_backtracks = len(versioned_package.split('/'))
    final_output_dir = os.path.join(path_to, versioned_package)
    os.system("cd " + final_path + " && git diff " + first_commit.hexsha + " | grep -v '^diff\|^index' | tee ." + patch_name + ".patch")
    if os.path.isdir(final_output_dir) and len(os.listdir(final_output_dir)) > 0:
        print("While sending the patch diff, another directory was found and it is not empty!")
        os.system('rm -rf ' + os.path.join(final_output_dir,'*'))
    os.makedirs(final_output_dir, exist_ok = True)
    shutil.move(os.path.join(final_path, '.' + patch_name + '.patch'), os.path.join(final_output_dir,  patch_name + '.patch'))
    return True


def strip_version(package_name) -> str:
    return re.sub('-[0-9.]+$', '', strip_version_tag(package_name))
    

def strip_version_tag(package_name) -> str:
    return re.sub('-r[0-9]+$', '', package_name)


# Here, we will do the tooling required for you to start patching a given package+version
# Then it unpacks your ebuild into it, and initializes the git repository for patching
# The container uses local user privileges as defined on your system for the uid you set this tool to use.
# Note: The repo name is NOT (yet) saved as part of the process.
def prep_patch(patch_name: str, package: str, version: str, force: bool, repo_name: str = '') -> bool:
    if not validate_package_format(package):
        print("Could not validate package name: " + package)
        return False
    repo_name = 'gentoo' if repo_name == '' else repo_name
    versioned_package           = package + '-' + version
    versioned_package_notag     = strip_version(versioned_package)
    patch_export_hostdir        = os.path.join(patches_workdir, patch_name)
    if os.path.isdir(patch_export_hostdir) and len(os.listdir(patch_export_hostdir)) != 0:
        print("A patch-in-progress workdir already is present at " + patch_export_hostdir + " and is not empty!")
        return False
    else:
        os.makedirs(patch_export_hostdir, exist_ok = True)
    # ebuild $(portageq get_repo_path / gentoo)/ package-category/package-name/package-name-version.ebuild clean unpack
    cmd_str = 'PORTAGE_TMPDIR="' + patches_export_mountpoint + '" ebuild $(portageq get_repo_path / ' + repo_name + ')/' + package + '/' + versioned_package.split('/')[-1] + '.ebuild clean unpack && cd ' + patches_export_mountpoint + ' && '
    #################################################################################################################################
    # BASIC IDEA:
    # Here, we will clean up the directory by removing all non source-code items.
    # However, we also preserve most of the directory structure so as to slip the whole thing into a portage directory when needed.
    # First, we make certain we have the source code dir to the base.
    # Then, we clean out the one other directory.
    # Finally, we move all the source code itself down to the base and delete the old source code directory. Done. :P
    #################################################################################################################################
    temp_sourcedir                  = os.path.join(patches_export_mountpoint, 'TEMP')
    final_destination               = os.path.join(patches_export_mountpoint, versioned_package)
    where_all_the_actual_code_is    = os.path.join(patches_export_mountpoint, 'portage', versioned_package, 'work', '*')  #re.sub('-', '.', versioned_package_notag.split('/')[-1].upper()))
    # Now we assemble the actual command string.
    # Now we can spin up a docker and unpack that patch into the workdir.
    #TODO Change to desired profile
    valid, profile = get_desired_profile()
    if valid:
        swap_stage(get_arch(), profile , 'gentoomuch/builder', False, patch_name)
    else:
        print("Prep patch: Could not get profile")
        return False
    print("PATCHING: " +
     "\n patch_export_hostdir: " + patch_export_hostdir +
     "\n patches_export_mountpoint " + patches_export_mountpoint + 
     "\n temp_sourcedir: "+ temp_sourcedir + 
     "\n final_destination: " + final_destination + 
     "\n where_all_the_actual_code_is: " + where_all_the_actual_code_is)
    # We build the cmd_str
    cmd_str += 'mkdir -p ' + temp_sourcedir + ' && '
    cmd_str += 'mv ' + where_all_the_actual_code_is + ' ' + temp_sourcedir + ' && '
    cmd_str += 'rm -rf ' + os.path.join(patches_export_mountpoint, 'portage') + ' && '
    cmd_str += 'mkdir -p ' + versioned_package + ' && '
    cmd_str += 'mv ' + os.path.join(temp_sourcedir, '*') + ' ' + final_destination + ' && '
    cmd_str += 'rm -rf ' + temp_sourcedir
    code = os.system('cd ' + output_path  + " && docker-compose run --user gentoomuch-user gentoomuch-patcher /bin/bash -c '" + cmd_str + "'")
    if code != 0:
        return False
    # This appends the git commands we use to initiate the users' patch-making process.
    versioned_package_basedir = os.path.join(patch_export_hostdir, versioned_package)
    print("PREP PATCH - " + versioned_package_basedir)
    for d in os.listdir(versioned_package_basedir):
        print("PREP PATCH: " + d)
    code = os.system('cd ' + os.path.join(versioned_package_basedir, d) + ' && git init && git add . && git commit -m "As-is from upstream (virgin.)"')
    # Debug messages.
    # print('Repo name:' + repo_name)
    # print("Unpacked sourcecode basedir: " + patches_export_mountpoint)
    # print('Pkg name (no tag): ' + versioned_package_notag)
    # print('Pkg name (with release tag): ' + versioned_package)
    # print('DEBUG: prep_patch(patch_name=' + patch_name + ', package=' + package + ', version=' + version + ', force=' + str(force) + ', repo_name=' + repo_name)
    # print("Patches mountpoint: " + patches_export_mountpoint)
    if code != 0:
        return False
    if not os.path.isdir(patches_workdir):
        code = os.makedirs(patches_workdir, exist_ok = True)
        if code == 0:
            pass
    return True


#def list_available_package_versions(package: str, repo_name = ''):
#    if not validate_package_format(package):
#        exit("Could not read package version")
#    repo_name = 'gentoo' if repo_name == '' else repo_name
#    cmd_str = 'ls -alh $(portageq get_repo_path / ' + repo_name + ')/' + package
#    code = os.system('cd ' + output_path + ' && docker-compose run -u ' + get_gentoomuch_uid() + " gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
    

def save_patch(patch_name : str) -> bool:
    p = os.path.join(saved_patches_path, patch_name)
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok = True)
    send_diff(patches_workdir, p, patch_name)
    return True




def try_patch(profile: str, patch_name : str) -> bool:
    valid, package_name = package_from_patch(patch_name)
    if not valid:
        print("Invalid patch name entered. Stopping.")
        return False
    patch_outdir = os.path.join(portage_output_path, 'patches')
    #print(patch_outdir)
    cmd_str = 'emerge --onlydeps =' + package_name + ' && '
    cmd_str += "emerge --usepkg n =" + package_name
    if valid:
        swap_stage(get_arch(), profile, 'gentoomuch/builder', False, str(patch_name))
        #code = os.system('cp -R ' + os.path.join(saved_patches_path, patch_name, '*') + ' ' + patch_outdir)#send_diff(patches_workdir, patch_outdir, patch_name)
        # create_composefile(output_path)
        # if code == 0:
        #     pass
        code = os.system("cd " + output_path + " && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
        if code == 0:
            pass
        return True
    print("TRY_PATCH:: Could not try patch " + patch_name)
    return False
