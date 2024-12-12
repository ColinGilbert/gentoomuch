#!/bin/bash

mkdir -p ~/gentoomuch-data &
mkdir -p ~/gentoomuch-data/{portage,stages,bootstrap,gpg} &&
mkdir -p ~/gentoomuch-data/portage/{blob,mountpoint} &&
touch ~/gentoomuch-data/profiles &&
echo 'gentoo-sources' > ~/gentoomuch-data/kernel-sources
