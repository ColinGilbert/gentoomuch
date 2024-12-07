#!/usr/bin/env bash

sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
#apt install docker.io -y
sudo apt install docker-compose python3-docker python3-gnupg python3-git -y
sudo usermod -a -G docker vagrant
gpg --keyserver hkps://keys.gentoo.org --recv-keys 13EBBDBEDE7A12775DFDB1BABB572E0E2D182910
