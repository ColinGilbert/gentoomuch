#!/bin/bash

rm -rf ./gentoomuch-data/* &&
mkdir ./gentoomuch-data/{portage,stages,bootstrap,gpg} &&
mkdir ./gentoomuch-data/portage/{blob,mountpoint}
