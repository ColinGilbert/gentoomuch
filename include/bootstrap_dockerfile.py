#!/usr/bin/env python3

import os
from .gentoomuch_common import dockerized_username, patches_mountpoint
from .get_gentoomuch_uid import get_gentoomuch_uid

def bootstrap_dockerfile(tarball_name: str, profile: str) -> str:
    results =  'FROM scratch\n'
    results += 'COPY --from=localhost:5000/gentoomuch-bootstrap:latest / /\n'
    results += 'COPY ' + tarball_name + ' /\n'
    results += 'WORKDIR /\n'
    results += 'RUN mkdir /mnt/stages \\\n'
    results += '&& mkdir /mnt/kernels \\\n'
    results += '&& mkdir /mnt/user-data \\\n'
    results += '&& mkdir /mnt/data-out \\\n'
    results += '&& mkdir /mnt/squashed-portage \\\n'
    results += '&& mkdir /mnt/gentoo \\\n'
    results += '&& mkdir /mnt/portage.imported \\\n'
    results += '&& rm -rf /etc/portage/package.use \\\n'
    uid = get_gentoomuch_uid()
    results += '&& groupadd -g 1000 ' + dockerized_username + '\\\n'
    results += '&& useradd -m -u ' + uid + ' -g ' + uid + ' -G portage ' + dockerized_username + ' \\\n'
    results += '&& mkdir ' + patches_mountpoint +  ' \\\n'
    results += '&& chown -R ' + uid + ':' + uid + ' ' + patches_mountpoint + '\n'
    # results += '&& USER ' + dockerized_username
    #results += 'WORKDIR /home/' + dockerized_username + '\n'
    results += 'CMD /bin/bash'

    return results
