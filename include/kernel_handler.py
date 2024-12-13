import os
from .gentoomuch_common import kernel_configs_path, kernel_defines_path, kconfigs_mountpoint, output_path
from .swap_stage import swap_stage


class kernel_handler:
    def __init__(self):
        self.name = ''
        self.version = ''
        self.release = ''
        self.good = False

    def from_canonical_name(self, name: str):
        elems = name.split('-')
        if len(elems) < 3 or elems[0] != 'linux':
            self.good = False
            return
        self.version = elems[1]
        self.name = elems[2]
        if len(elems) > 3:
            if elems[3].startswith('r'):
                tag = elems[3]
                self.release = tag[1:]
        self.good = True

    def from_package_name(self, name: str):
        elems = name.split('-')
        if len(elems) < 3:
            self.good = False
            return
        self.name = elems[0]
        self.version = elems[2]
        if len(elems) > 3:
            if elems[3].startswith('r'):
                tag = elems[3]
                self.release = tag[1:]
        self.good = True

    def get_canonical_name(self): # linux-6.12.4-gentoo-r1
        return 'linux-' + self.version + '-' + self.name + (('-r' + self.release) if self.release != '' else '')

    def get_package_name(self): # gentoo-sources-6.12.4-r1
        return self.name + '-sources-' + self.version + (('-r' + self.release) if self.release != '' else '')

    def prep_kernel_config(self, arch: str, desired_profile: str, kernel_defines_name: str):
        self._ingest_kernel_config(kernel_defines_name)
        self.download_kernel(arch, desired_profile, kernel_defines_name)
        cmd_str = "cd /usr/src && "
        cmd_str += "ln -sf " + self.get_canonical_name() + " " + self.kernel_path + " && "
        cmd_str += "cd " + self.kernel_path + " && "
        kconf_exists = os.path.isfile(self.host_kconf_path)
        if kconf_exists:
            cmd_str += "cp " + self.mounted_kconf_path + " " + self.active_kconf_path + " && "
            cmd_str += "make nconfig && "
            cmd_str += "cp " + self.active_kconf_path + " " + self.mounted_kconf_path
        else:
            cmd_str += "make nconfig && "
            cmd_str += "cp " + self.active_kconf_path + " " + self.mounted_kconf_path
        swap_stage(arch, desired_profile, "gentoomuch/builder", False) 
        code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
        if code == 0:
            pass

    def download_kernel(self, arch: str, profile: str, kernel_defines_name: str):
        self._ingest_kernel_config(kernel_defines_name)
        cmd_str = 'cd /usr/src && if [ ! -d ' + self.get_canonical_name() + ' ]; then '
        cmd_str += 'emerge --onlydeps =' + self.get_package_name() + ' && '
        cmd_str += 'emerge --oneshot --usepkg n =' + self.get_package_name()
        cmd_str += '; else '
        cmd_str += 'echo "ALREADY DOWNLOADED KERNEL"'
        cmd_str += '; fi'
        swap_stage(arch, profile, "gentoomuch/builder", False)
        code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")
        if code == 0:
            pass        

    def build_kernel(self, arch: str, profile: str, jobs: int, kernel_defines_name: str):
        self._ingest_kernel_config(kernel_defines_name)
        cmd_str = "cd /usr/src && "
        cmd_str += "ln -sf " + self.get_canonical_name() + " " + self.kernel_path + " && "
        kconf_exists = os.path.isfile(self.host_kconf_path)
        if kconf_exists:
            cmd_str += "cp " + self.mounted_kconf_path + " " + self.active_kconf_path + " && "
            cmd_str += "cd " + self.kernel_path + " && "
            cmd_str += 'emerge --onlydeps =' + self.get_package_name() + ' && '
            cmd_str += "make -j" + str(jobs)
            swap_stage(arch, profile, "gentoomuch/builder", False)
            code = os.system("cd " + output_path + " && docker-compose up --quiet-pull --no-start && docker-compose run gentoomuch-builder /bin/bash -c '" + cmd_str + "'")  
            if code == 0:
                pass
        else:
            exit("A valid kernel config file is required to build ka ernel")

    def wipe_all_kernels(self):
        pass

    def _ingest_kernel_config(self, kernel_defines_name: str):
        self.specific_kernel_defines_path = os.path.join(kernel_defines_path, kernel_defines_name)
        self.specific_kernel_defines_config_path = os.path.join(self.specific_kernel_defines_path, 'config')
        self.specific_kernel_defines_sources_path = os.path.join(self.specific_kernel_defines_path, 'sources')
        defines_exists = os.path.isdir(self.specific_kernel_defines_path) and os.path.isfile(self.specific_kernel_defines_config_path) and os.path.isfile(self.specific_kernel_defines_sources_path)
        if defines_exists:
            with open(self.specific_kernel_defines_config_path) as file:
                config_name = file.read().strip()
            with open(self.specific_kernel_defines_sources_path) as file:
                sources_name = file.read().strip()
            self.from_package_name(sources_name)
            config_filename = config_name + ".kconf"
            self.host_kconf_path = os.path.join(kernel_configs_path, config_filename)
            self.mounted_kconf_path = os.path.join(kconfigs_mountpoint, config_filename)
            self.kernel_path = "/usr/src/linux"
            self.active_kconf_path = "/usr/src/linux/.config"
        else:
            exit("Could not find correct kernel definition in " + self.specific_kernel_defines_path)


def test_kernel_handler():
    test = kernel_handler()
    canonical_name = 'linux-6.12.4-gentoo-r1'
    package_name = 'gentoo-sources-6.12.4-r1'
    test.from_canonical_name(canonical_name)
    if canonical_name == test.get_canonical_name():
        print('SUCCESS - Canonical name')
    else:
        print('FAILURE - Canonical name: ' + test.get_canonical_name())
    if package_name == test.get_package_name():
        print("SUCCESS - Package name")
    else:
        print('FAILURE - Package name')
    test.from_package_name(package_name)
    if package_name == test.get_package_name():
        print('SUCCESS - Package name 2')
    else:
        print('FAILURE - Package name 2')
    if canonical_name == test.get_canonical_name():
        print('SUCCESS - Canonical name 2')
    else:
        print('FAILURE - Canonical name 2')