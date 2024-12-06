from .gentoomuch_common import profiles_path

def save_profiles(profiles):
    f = open(profiles_path, 'w')
    f.writelines(profiles)