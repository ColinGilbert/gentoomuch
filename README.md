Gentoomuch: Immutable, repeatable Gentoo
========================================

Intro:
------

I absolutely _fell in love_ with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by consensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. The significant advantage of a tailored operating system is that things remain in harmony. However, unless carefully managed, a source-based distribution such as Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This tool provides automations to enable such careful management. Using Gentoomuch allows any user to be brave... If you use source control on the config directory, then congratulations: your builds are now reproducible. Gentoo and DevOps are coming closer together. This tool's purpose is to create custom Gentoo-based stage4 tarballs. It was made with immutable machines in mind.

Gentoomuch allows Gentoo users to reversibly experiment with unknown use-flag combinations and easily create patches for broken packages. Gentoomuch allows long-time developers another means to orchestrate their build processes. It gives Gentoo sysadmins a modern way to reduce technical debt. It gives cloud engineers the option of using highly-optimized, immutable Gentoo for their virtualized servers. Using this tool is a rather civilized way of managing multiple Gentoo installations; it has very good amenities. It was made to be played with.

Gentoomuch allows you manage an entire network's worth of Gentoo systems without fuss, while still being fun to use!

Gentoo Linux has been cast as intimidating and error-prone. This tool aims to remove the bad by ensuring that all your builds are from a known state, and by offering you an easy way to define and build multiple systems! We use Docker-Compose to maintain a clean working environment on every run. The software can create an optimized builder directly from any of the publicly-available stage3 tarballs. 

Gentoomuch aims to to dovetail into the existing ecosystem by being very carefully designed for minimum intrusiveness: Due to being greatly inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to existing users. The tool also feels a bit like using the Docker command and that is no coincidence.

Gentoomuch supports the important use-case of prepping and using patches when a package breaks. Gentoomuch does all the unpacking and diffing and file copying for you. That way, you can have a working system until upstream gets its act together! ;) Pro tip: If you want them to fix the problem, report the issue on Bugzilla and send them the patch once you know it works.

I think this code generally represents best practices for juggling multiple systems in everyone's favourite meta-distribution. Nothing is ever perfect and since upstream is a moving target, there will always be something to do. Not to mention that you can always find a list of best practices with conflicting advice: Choices were made. However, this toolkit is solid: Even when this thing was only half-built, working with Portage was already a saner experience for me than it had ever been beforehand. I hope you find Gentoomuch useful, too.

This tool was _made_ to be played with.

What's the catch?
-----------------

Nothing ever comes completely cost-free - If you are an existing (ie: skeptical) Gentoo user asking yourself whether or not this tool is worth your while, I will be upfront about the limitations:

- This tool presupposes that you are proficient in Gentoo and Linux in general. If you're a beginner you should try running Gentoo locally before you start automating your builds.
- The Gentoomuch pipeline takes more time than if you were to simply run emerge on your local system. In exchange, you get robustness, repeatability, and automation.
- Portage hates not being in control of the kernel sources (especially when compiling/signing kernel modules), so we limit the user to a single version of gentoo-sources, which can be modified in gentoomuch/builder's local portage config files. 
- Your workflow will change a bit. Mostly it'll mean defining your sets of packages/flags and then defining your machines from these sets, instead of directly within /etc/portage on each machine.
- You have to add flags manually to your configs (ie: copy and paste from emerge output.) Using ``--autounmask-write`` and running ``dispatch-conf`` does't work in a pipeline that uses immutable containers.
- When making builder images, Gentoomuch keeps the tarball inside the image instead of deleting it as upstream does with their Docker images. This does entail an additional cost of space. However, you then benefit by completely avoiding the chicken-and-egg problem!
- Bootstrapping dockerized images, epsecially for the first time, can take a while. This is because we do ``emerge --emptytree`` with ``ROOT=/mnt/gentoo`` (which points to a temporary environment.) This makes Portage re-emerge each package twice, once for ``/`` and once for ``/mnt/gentoo``. This is a possible bug in emerge and I'll be talking to upstream about that.
- For some silly reason, ``gentoo-sources`` gets re-emerged on every pipeline invocation. I consider this a bug to be fixed and welcome any input from the community as to why this keeps happening.
- Patches are limited to a single version of a package. This is because patches should be one-offs. If you want something more permanent, you should create an ebuild.

Usage notes:
------------

Your configuration lives in the ``~/gentoomuch-config`` directory.
A configuration called "gentoomuch/builder" exists. Modify it when you need to; I made the decision to expose every possible configuration to the end-user. 
Further documentation is in the config directory. These aforementioned folders are intended to be both part of our pipeline and as living, implicitly-tested documentation for anyone looking to get started.

CLI Reference:
--------------

- ``gentoomuch init``: Initializes the ``~/gentoomuch-data`` directory. If tmpfs is mounted to it, then you need to run this command every boot. 
- ``gentoomuch freshroot``: Drops you into a builder environment. Here, you can test out different use-flags for emerging, etc.
- ``gentoomuch pipeline``: Runs the pipeline. It'll build all stage4s defined in ``~/gentoomuch-config``.
- ``gentoomuch sync``: Runs emerge --sync.
- ``gentoomuch bootstrap <profile.name> <tarball.filename>``: Bootstraps a builder from an upstream stage3 ands its corresponding .asc signature, for a profile you define.
- ``gentoomuch profile ls``: Lists the profiles you've bootstrapped.
- ``gentoomuch profile set <profile.name>``: Sets the profile that'll be used when calling ``freshroot``
- ``gentoomuch stage build <stage4.definition>``: Builds a stage4 that you've defined. This for you to test a build before running the whole pipeline.
- ``gentoomuch kernel prep <kernel.config>``: Prepares a named kernel config and drops you into ``make nconfig``. If the configuration doesn't exist, Gentoomuch creates a new one. 
- ``gentoomuch kernel update``: Deletes all downloaded kernel source files and re-download fresh ones.
- ``gentoomuch patch prep <patch.name> <package.name> <version-str>``: Sets up a patch directory in ``~/gentoomuch-data/patches.work/patch.name``. You then modify the files within it according to your needs.
- ``gentoomuch patch try <patch.name>``: Tries to compile the patch in your patches working directory.
- ``gentoomuch patch save <patch.name>``: Saves a patch to ``~/gentoomuch-config/user.patches/patch.name``.
- ``gentoomuch patch compile``: Compiles all patches.
- ``gentoomuch clean``: Cleans up temporary files.

Prerequisites:
--------------

- You need a Linux host. Currently I'm using Ubuntu to bootstrap, but Gentoo with the correct packages is another platform that will work. In fact, Gentoo is the final target for deployment. 
- You need that have ``sudo``, ``python``, ``gpg``, ``pigz``, ``tar``, ``rsync``, ``python-docker`` (Ubuntu)/``dev-python/docker`` (Gentoo), ``gitpython``, `python-gnupg`, ``docker``, ``buildx``, and ``docker-compose`` installed.
- You need a default gpg signing key for your user in order to sign stages. You can also use a smartcard. 

Installation:
-------------

- Run ``gpg --keyserver hkps://keys.gentoo.org --recv-keys 13EBBDBEDE7A12775DFDB1BABB572E0E2D182910`` to get the Gentoo stage3 signing key.
- Clone this repository. Append it to your PATH variable.
- Clone the [gentoomuch-config repository](https://github.com/ColinGilbert/gentoomuch-config) to your home directory.
- (Optional) Create a ``gentoomuch-data`` directory in your home directory and set it to mount tmpfs.
- Run ``gentoomuch init``
- Create a CPU definition in ``~/gentoomuch-config/cpu.defines``
- Edit ``~/gentoomuch-config/stage3-defines/gentoomuch/builder/cpu`` to point to that CPU definition.
- Download a stage3 of your architecture and its .asc signature from upstream and run ``gentoomuch bootstrap <profile-name> stage3-*.tar.xz`` and wait for the first emerge.
- Once it's done, you should be good to go!

I will be creating packages for Gentoo and possibly Ubuntu in the near future. Stay tuned for updates!

Roadmap:
--------

- Support for vanilla-sources and others
- Cloud platform support (AWS first)
- UEFI secure boot kernel signing