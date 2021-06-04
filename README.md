<h2>GentooMuch: Because something like this was bound to happen...</h2>

<h3>Intro:</h3> I absolutely <i>fell in love</i> with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. I originally switched to Gentoo because Ubuntu at the time was giving me so much grief with video drivers, and I never looked back. The significant advantage of a tailored operating system is as things remain in harmony. However, unless carefully managed, a source-based distribution such as Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This toolkit provides automations to enable such careful management. Using Gentoomuch allows any user to be brave... If you use source control on the ``config`` directory, then congratulations: your builds are now reversible!

<h3>GentooMuch allows you manage an entire network's worth os Gentoo systems without fuss, while still being fun to use!</h3>
Gentoo Linux has been cast as intimidating and error-prone, and this toolkit aims to remove the bad by ensuring that all your builds are done from a known state and by offering you a way to define multiple systems. We use Docker-Compose to maintain a clean working environment on every run. The software creates an optimized buildmaster (and before long, ccache support and optional distcc workers) directly from any of the publicly-available Gentoo stages from upstream. However, this toolkit also keeps the good parts of Gentoo; it is a <i>fun</i> little toolkit!

The Gentoo Project has existing tools for reliably bootstrapping stages, but these <i>development</i> tools are ill-suited to the task of customizing a network's worth of installations. GentooMuch aims to to dovetail into the existing upstream ecosystem by being very carefully designed for productionr: Due to being greatly inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to existing users. The tool also feels a bit like using the Docker command, and that is no coincidence either. More importantly, I didn't want this tool to jam up the workflow: As such, if a feature cannot be implemented unobtrusively it doesn't belong here.

GentooMuch allows Gentoo users to reversibly experiment with unknown use-flag combinations and easily create patches for broken packages; once the public API gets developed, it'll be the ideal tool for shakedown testing. GentooMuch allows long-time developers another means to orchestrate their own build processes.  It gives sysadmins who must juggle entire networks a modern way to reduce technical debt. Using this tool is a rather civilized way of managing multiple Gentoo installations.

<h3>This tool is just made to be played with.</h3> In fact, once you setup, you select your profile with ``gentoomuch profile ls``, set it with ``gentoomuch profile set <name>`` and then you can bootstrap with ``gentoomuch bootstrap``. Afterwards, you can pull up a fresh stage3 environment with ``gentoomuch freshroot`` and start emerging packages right away! It'll keep the built ones so you won't have to recompile them from scratch again. For example, if upstream has a package broken on the minimalistic and marginally-supported libc you're using on your router and you need to quickly make it work, just go ``gentoomuch patch prep <name> <package> <version>``. You work in the directory that gets automatically prepared for your convenience, and then youtry compiling the patched package with ``gentoomuch patch try <name>`` until it works. Once you're done, just use ``gentoomuch patch save <name>`` and you'll be able to make use of it across any of your builds - you'll either place it in one of your parent configs, or just use it for all affected profiles until upstream gets its act together! Pro tip: Send them the patch once you know it works.

Packages are by default compiled with FEATURES="binpkg-multi-instance buildpkg usepkg", which allows a single binpkg directory to provide for all your systems out-of-the-box! This minimizes the amount of compilation required and keeps your systems available for running tests, numbercrunching for extra-terrestrials, or mining Monero.

<h4>Usage notes.</h4>
- Everything you keep is in the ``config`` directory; the rest is either an executable file, or documentation, or temporary. Also, many subdirectories within ``config`` have within them another one called ``gentoomuch``, and everything in those is reserved: Changing anything in there will likely break your builds, so I don't generally recommend it.
- Further documentation is in the config directory. Our aforementioned ``gentoomuch`` folders are intended to be both part of our pipeline's configuration and as living, implicitly-tested documentation for someone looking to get started.

<h4>What's the catch?</h4> Nothing ever comes completely cost-free - If you are an existing (ie: skeptical) Gentoo user asking yourself whether or not this tool is worth your while, I will be upfront about the limitations:
- Your workflow will change a bit and you'll want to look at ``./config/README.md``. Mostly it'll mean creating subdirectories for your sets of packages/flags and then defining your machines from these sets, instead of directly within ``/etc/portage``
- When building stage3 Docker images, GentooMuch keeps the tarball inside instead of deleting it as upstream does with theirs. This entails a cost in space, but also prevents a chicken-egg sitation.
- GentooMuch is currently being developed on AMD64 systems but support for others will come very, very soon.

I think this code generally represents best practices for maintaining multiple systems in our favourite meta-distribution; nothing is ever perfect and there are a few things I might implement to optimize for certain tasks, but this toolkit is solid. Even when this thing was only half-built working with Portage was already a better, far saner experience.
