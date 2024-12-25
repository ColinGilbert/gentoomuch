import os
from .exec_in_chroot import exec_in_chroot
from .gentoomuch_common import user_scripts_path, user_removes_path, chroot_workdir
from .sign_stage import sign_stage
from .verify_tarball import verify_tarball

def exec_user_hooks(stage_path: str, scripts: [str], removes: [str]):
    if not verify_tarball(stage_path):
        print("EXEC USER HOOKS: COULD NOT VERIFY STAGE")
        return False
    code = os.system('mkdir -p ' + chroot_workdir + ' && rm -rf ' + os.path.join(chroot_workdir, '*') + ' && tar xpf ' + stage_path + ' -C ' + chroot_workdir)
    if code == 0:
        pass
    if len(scripts) > 0:
        scripts_fullpath = []
        for s in scripts:
            if s == "README.md":
                continue
            scripts_fullpath.append(os.path.join('/mnt/user.scripts', s))
        results = exec_in_chroot(chroot_workdir, ' && '.join(scripts_fullpath))
        if not results:
            print("EXEC USER HOOKS: Chroot command failed")
            # code = os.system('sudo rm -rf ' + chroot_workdir)
            # if code == 0:
            #     pass
            return False
    if len(removes) > 0:
        removes_fullpath = []
        for l in removes:
            if l == "README.md":
                continue
            if not os.path.isfile(os.path.join(user_removes_path, l)):
                exit("EXEC USER HOOKS: Could not find " + os.path.join(user_removes_path, l))
            with open(os.path.join(user_removes_path, l)) as file:
                list_contents = file.readlines()
            for ll in list_contents:
                removes_fullpath.append(os.path.join(chroot_workdir, ll))
        remove_commands = []
        for r in removes_fullpath:
            if r == "README.md":
                continue
            remove_commands.append('rm -rf ' + r)
        print("EXEC USER HOOKS: Removing " + " ".join(removes_fullpath))
        code = os.system(' && '.join(remove_commands))
        if not code == 0:
            print("EXEC USER HOOKS: Removes failed")
            # code = os.system('sudo rm -rf ' + chroot_workdir)
            # if code == 0:
            #     pass
            return False
    code = os.system('rm -rf ' + stage_path + ' && cd ' + chroot_workdir + " && tar --exclude='./dev/*' -cf " + stage_path + " . --use-compress-program=pigz --xattrs --selinux --numeric-owner --acls")
    if code == 0:
        pass
    code = os.system('sudo rm -rf ' + chroot_workdir)
    if code == 0:
        pass
    results = sign_stage(stage_path)
    return results