Note: Master branch only has initial work - almost everything is in dev; it will be merged within the next few days.

Gentoo Linux has been cast as intimidating and error-prone. This toolkit aims to remove much of the error-prone parts by ensuring all your builds can be repeated. However, it does not get in the way; if it feels exactly like using Gentoo, its because you're using Gentoo.

'I absolutely fell in love with Gentoo Linux several years ago.' It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. People often speak of Gentoo as a speed-freaks' OS, but I originally switched over because Ubuntu 12.04 was giving so much grief with the NVidia drivers that Gentoo was actually _far easier_ to install. I have since compared every OS to a well-configured Gentoo system.

There are significant advantages to be had in working with a tailored operating system: a minimized set of moving pieces can stay in harmony forever. However, unless carefully managed a Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This tool provides much, if not most, of that careful management.

This tool allows Gentoo users to reversibly try previously unknown use-flag combinations. It allows long-time developers another opetion to automate their own work, and affords the sysadmins who must juggle entire networks a modern possibility to reduce technical debt. It aims to pick up where Gentoo's Catalyst/Crossdev stop and where programming-in-the-large begins.

Zentoo is Gentoo with a paper-thin abstraction layer that builds/packs stages and kernels. We use Docker Compose (multinode Swarm coming very soon!) to maintain a clean working environment on every run. The software creates an optimized buildmaster (and optional distcc workers) from any of the publicly-available Gentoo stages. These are subsequently used to compile other packages. In fact, you can pull up a new stage3 environment with ./freshroot and start work on compiling a fresh set of packages right away, unbound by any prior cruft. The next time you get into an environment it'll keep the built package and you won't have te recompile it from scratch again. We remount our multi-instance binpkg repo, and away we go! Coming soon will be automatic cleanup, repairs, and tmpfs caching for the best experience! I use this software as a daily driver and await your feedback with open arms and ears. Zentoo aims to be a production tool: Due to being inspired by Gentoo's existing workflows, its patterns are implicitly relatable to existing users.

'Zen emphasizes' (1) rigorous self-restraint, (2) meditation-practice, (3) insight into the nature of mind and things, and (4) the expression of this insight in daily life (5) especially for the benefit of others.
(Adapted from Wikipedia)

I believe Zentoo mirrors these ideals: This form (1) imposes rigorous restraint over your build process to keep them sane over extended periods of time. (2) It is the product of constant practice and meditation (3) upon the nature of how people and computers work. From these insights, (4) This tool is very practical for day-to-day life. (5) Zentoo has been created to benefit the public good.

Packages are compiled with FEATURES="binpkg-multi-instance buildpkg", which allows a single package repository to be shared across all hosts. Hosts that assemble aren't given write-access to the package repository and use "binpkg-only." This allows, for example, a glibc-based host to compile musl and uclibc versions of a tool that wouldn't otherwise be available on their respective Portage profiles due to unmet dependencies!

While still in its first few days of development, this tool has already proven a far smoother and more reliable experience than any of my past methods. It is currently being developed and tested on AMD64 systems but ARM64 support is coming soon. However, this toolkit can run on anything Docker-Compose can drive and that Gentoo creates stages, so it should seamlessly port to any platform supported by the Gentoo Project on Dockerhub. Building this toolkit was a a fun challenge and a lovely excuse to learn Docker's ecosystem in-depth, and I genuinely hope you enjoy the results.

Happy developement/sysops/playtime!




User tasks:
1) For each root, define your /etc/portage directory as a named branch in config/portage. Put in your use-flags and everything!
2) If needed, define buildhooks as a named branch in config/buildhooks.
3) Define package sets in the config/portage/sets directory. https://wiki.gentoo.org/wiki/Package_sets#User_defined_sets
4) Define system tuples (``<portage>-<buildhooks>-<packages>``) in config/tuples.

Something worth noting is that the first two tasks require a git branch every time you save changes, whereas the latter two do not:
- This is because the first two tasks' file hierarchies remain mostly static duplicates of one another.
- The first two settings only concern a single root at one time: Our build system can go to a given branch, do its work, and restart with another.
- The entire set of configurations a user builds is unique to both their task and the hardware on-hand.
- It also represents the initial state of an entire network: much of it tends to be confidential.
- In contrast, system images (by default) aren't packed with _any_ private data.
- They also run on any similar-enough hardware, so they tend to be shared already. Using git to shoot those configs around the internet is what open-source is all about; if you're _that_ concerned, you likely already have an air-gapped system or proxies to help protect you.
- System images almost always end up in the possession of the end-user; confidentiality losses are basically nil because you're too smart to put all your secrets unencrypted into your OS image, right? :)
- Branching at the package-set and system tuples level is possibler. However, checking out is done by the user prior to running this tool.


Implementation details:

Our docker-compose file creates persistent volumes for:
```
/var/cache/binpkg
/var/cache/distfiles
/var/db/repos/gentoo
```
