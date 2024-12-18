#!/usr/bin/env python3

import os, re
from include.gentoomuch_common import output_path
from include.download_tarball import download_tarball
from include.gpg_setup import gpg_setup
from include.verify_tarball import verify_tarball
from include.create_composefile import create_composefile

#gpg_setup()
#download_tarball('amd64', 'default')
#download_tarball('amd64', 'musl-hardened')
create_composefile(output_path)
