import os

def send_kconf_tO_staging(kconf: str):
    host_kconf_path = os.path.join(kernel_configs_path, kconf)
    mounted_kconf_path = os.path.join(kconfigs_mountpoint, kconf)
    code = os.system("cp " + host_kconf_path + " " + mounted_kconf_path)
    if code == 0:
        return True
    return False 