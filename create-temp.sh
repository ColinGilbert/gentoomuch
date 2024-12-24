#!/bin/bash

mkdir -p ~/gentoomuch-data &
mkdir -p ~/gentoomuch-data/{portage,stages,bootstrap,squashed_ports,squashed_ports_host_mountpoint} &&
mkdir -p ~/gentoomuch-data/portage/{blob,mountpoint} &&
touch ~/gentoomuch-data/profiles &&
echo 'gentoo-sources' > ~/gentoomuch-data/kernel-sources
