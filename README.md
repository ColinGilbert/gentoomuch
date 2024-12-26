Gentoomuch: Because something like this was bound to happen...

Intro:

I absolutely fell in love with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by consensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. The significant advantage of a tailored operating system is that things remain in harmony. However, unless carefully managed, a source-based distribution such as Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This tool provides automations to enable such careful management. Using Gentoomuch allows any user to be brave... If you use source control on the config directory, then congratulations: your builds are now reproducible. Gentoo and DevOps are coming closer together. This tool's purpose is to create custom Gentoo-based stage4 tarballs. It was made with immutable machines in mind.

Gentoomuch allows Gentoo users to reversibly experiment with unknown use-flag combinations and easily create patches for broken packages. Gentoomuch allows long-time developers another means to orchestrate their own build processes. It gives sysadmins who must juggle entire networks a modern way to reduce technical debt. Using this tool is a rather civilized way of managing multiple Gentoo installations; it has very good amenities.

Gentoomuch allows you manage an entire network's worth of Gentoo systems without fuss, while still being fun to use! Gentoo Linux has been cast as intimidating and error-prone, and this tool aims to remove the bad by ensuring that all your builds are from a known state and by offering you an easy way to define and build multiple systems! We use Docker-Compose to maintain a clean working environment on every run. The software creates an optimized buildmaster directly from any of the publicly-available stage3s. However, this tool also keeps the best part of Gentoo; it is a <i>fun</i> little tool!

Gentoomuch aims to to dovetail into the existing ecosystem by being very carefully designed for minimum intrusiveness: Due to being greatly inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to existing users. The tool also feels a bit like using the Docker command and that is no coincidence.

Gentoomuch was made to be played with. In fact, to setup, just download your stage3 and .asc, then call ``gentoomuch bootstrap profile_name stage3-*.tar.xz``. This creates an optimized builder. You then enter into an fresh sandbox environment with ``gentoomuch freshroot`` and start emerging packages right away! It'll keep the built ones so you won't have to recompile them from scratch again.

We support the important use-case of prepping and using patches when a package breaks; if upstream has a package broken on the minimalistic and marginally-supported libc you're using on your tricked-out system, and you need to quickly make it work, just go ``gentoomuch patch prep``.
You work in the directory that gets automatically prepared for your convenience ``~/gentoomuch-data/patches`` and then you try compiling the patched package with``gentoomuch patch compile`` until it works. Once you're done, just use ``gentoomuch patch save`` and you'll be able to make use of it across all of your profiles.

It does all the unpacking and diffing and file copying for you. That way, you can have a working system until upstream gets its act together! ;) Pro tip: If you want them to fix the problem, report the issue on Bugzilla and send them the patch once you know it works...

Usage notes:

Everything you keep is in the ``config`` directory; the rest is either an executable file/deps, or documentation, or temporaries. A configuration called "gentoomuch/builder" exists. Modify it when you need to; I made the radical decision to expose every possible configuration to the end-user.  
Further documentation is in the config directory. These aforementioned folders are intended to be both part of our pipeline and as living, implicitly-tested documentation for anyone looking to get started.

What's the catch?

Nothing ever comes completely cost-free - If you are an existing (ie: skeptical) Gentoo user asking yourself whether or not this tool is worth your while, I will be upfront about the limitations:

- This tool presupposes that you know Gentoo quite well. If you're a beginner you should try running a system locally before upgrading to automation.
- The Gentoomuch pipeline takes more time than if you were to simply run emerge on your local system. In exchange, you get robustness, repeatability, and automation.
- Portage hates not being in control of the kernel sources (especially when compiling/signing kernel modules), so we limit the user to a single version of gentoo-sources, which can be modified in gentoomuch/builder's local portage config files. Support for vanilla-sources and others is planned for a future release.
- Your workflow will change a bit. Mostly it'll mean defining your sets of packages/flags and then defining your machines from these sets, instead of directly within /etc/portage.
- You have to add flags manually to your configs (ie: copy and paste from emerge output.) Using --autounmask-write and running dispatch-conf does't work in a pipeline that uses immutable containers.
- When building stage3 Docker images, Gentoomuch keeps the tarball inside the image instead of deleting it as upstream does with theirs. This does entail an additional cost of space. However, you then benefit by completely avoiding the chicken-and-egg problem!
- Bootstrapping dockerized images, epsecially for the first time, can take a while. This is because we do emerge --emptytree with ROOT=/mnt/gentoo which makes Portage re-emerge each package twice, once for / and once for /mnt/gentoo. This is a possible bug in emerge and I'll be talking to upstream about that.
- For some silly reason, gentoo-sources gets re-emerged on every pipeline invocation. I consider this a bug to be fixed and welcome any input from the community as to why this keeps happening.
- Patches are limited to a single version of a package. This is because patches should be one-offs. If you want something more permanent, you should create an ebuild.
- You need that have installed sudo, pigz, tar, rsync, docker-python, git-python, and docker-compose.

I think this code generally represents best practices for maintaining multiple systems in everyone's favourite meta-distribution. Nothing is ever perfect and since upstream is a moving target, there will always be something to do. Not to mention that you can always find a list of best practices with conflicting advice: Choices were made. However, this toolkit is solid: Even when this thing was only half-built, working with Portage was already a saner experience for me than it had ever been beforehand. I hope you find Gentoomuch useful, too.