from .gentoomuch_common import profiles_path

def save_profiles(profiles):
    f = open(profiles_path, 'w')
    for p in profiles:
        p = p.strip()
        p += '\n'
        f.write(p)
    f.close()