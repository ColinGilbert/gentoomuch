import os
import gnupg
from hashlib import sha512, blake2b

def sign_stage(path: str):
    if not os.path.isfile(path):
        exit("SIGN STAGE: Could not find file at " + path)
    code = os.system("rm " + path + ".asc & gpg --sign --detach-sig --armor " + path)
    if code != 0:
        return False
    return True