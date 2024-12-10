<p>
STATUS: Currently updating it to work correctly after three years' hiatus

</p>
<h3>GentooMuch: Because something like this was bound to happen...</h3>

<h4>Intro:</h4>
<p>
I absolutely <i>fell in love</i> with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. The significant advantage of a tailored operating system is as things remain in harmony. However, unless carefully managed, a source-based distribution such as Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This toolkit provides automations to enable such careful management. Using Gentoomuch allows any user to be brave... If you use source control on the config directory, then congratulations: your builds are now reversible. Gentoo and DevOps are making babies!
</p>
<p>
GentooMuch allows Gentoo users to reversibly experiment with unknown use-flag combinations and easily create patches for broken packages; once the public API gets developed, it'll be the ideal tool for shakedown testing. GentooMuch allows long-time developers another means to orchestrate their own build processes. It gives sysadmins who must juggle entire networks a modern way to reduce technical debt. Using this tool is a rather civilized way of managing multiple Gentoo installations; it has very good amenities.
</p>
<h4>GentooMuch allows you manage an entire network's worth of Gentoo systems without fuss, while still being fun to use!</h4>
Gentoo Linux has been cast as intimidating and error-prone, and this toolkit aims to remove the bad by ensuring that all your builds are from a known state and by offering you an easy way to define and build multiple systems! We use Docker-Compose to maintain a clean working environment on every run. The software creates an optimized buildmaster directly from any of the publicly-available profiles. However, this toolkit also keeps the best part of Gentoo; it is a <i>fun</i> little toolkit!
<p>
GentooMuch aims to to dovetail into the existing ecosystem by being very carefully designed for minimum intrusiveness: Due to being greatly inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to existing users. The tool also feels a bit like using the Docker command and that is no coincidence. I didn't want this tool to jam up a workflow.
</p>
<h4>This tool is just made to be played with.</h4>
In fact, to setup, just download your stage3, .DIGEST, and .asc, and call
<pre>gentoomuch bootstrap profile_name stage3-*.tar.xz</pre>
This creates an optimized builder, which will benefit from all future improvements to this build system. You then enter into an fresh sandbox environment with
<pre>gentoomuch freshroot</pre>
and start emerging packages right away! It'll keep the built ones so you won't have to recompile them from scratch again.
</p>
<p>
We support the important use-case of prepping and using patches when your profile breaks; if upstream has a package broken on the minimalistic and marginally-supported libc you're using on your tricked-out home router or your edge-case FPGA-optimized system, and you need to quickly make it work, just go
<pre>gentoomuch patch prep</pre>
You work in the directory that gets automatically prepared for your convenience, ./gentoomuch-data/patches.in.progress and then you try compiling the patched package with
<pre>gentoomuch patch try</pre>
until it works. Once you're done, just use
<pre>gentoomuch patch save</pre>
and you'll be able to make use of it across all of your profiles.
<p>
It does all the unpacking and diffing and file copying for you. That way, you can have a working system until upstream gets its act together! ;) Pro tip: If you want them to fix the problem, send them the patch once you know it works...
</p>
<p>
Packages get all their dependencies automatically unmasked so as to not force you to pollute your Portage config. If you seek to avoid a given package or to force usage of a given version, you are able to do so by creating another directory in
</pre>portage.locals</pre>
<p>
We also use a multi-instanced binpkg directory to provide for all your systems out-of-the-box! This minimizes the amount of compilation required and keeps your compute power available for running tests, numbercrunching for extra-terrestrials, or mining Monero.
</p>
<h4>Usage notes.</h4>
<ol>
<li>Everything you keep is in the
</pre>config</pre>
directory; the rest is either an executable file/deps, or documentation, or temporaries. A number of configurations have within them another called "gentoomuch." Everything inside these is reserved: Changing anything in there will likely break your builds, so I don't generally recommend doing so unless you're willing to debug thing by yourself.
</li>
<li>Further documentation is in the config directory. These aforementioned folders are intended to be both part of our pipeline and as living, implicitly-tested documentation for anyone looking to get started.</li>
</ol>
<h4>What's the catch?</h4>
Nothing ever comes completely cost-free - If you are an existing (ie: skeptical) Gentoo user asking yourself whether or not this tool is worthwhile, I will be upfront about the limitations:
<ol>
<li>Your workflow will change a bit. Mostly it'll mean creating subdirectories for your sets of packages/flags and then defining your machines from these sets, instead of directly within /etc/portage, Also, you now access your build environments by using the freshroot command.
</li>
<li>When building stage3 Docker images, GentooMuch keeps the tarball inside instead of deleting it as upstream does with theirs. This does entail an additional cost of 200-300MiB of disc space per profile you bootstrap on your local machine. However, you then benefit by completely avoiding the chicken-and-egg situation!
</li>
<li>Responsiveness is a bit less snappy than a pure chroot, but the vast majority is your wait will be limited to the time when you'll bootstrapping a dockerized image... The rest is a joke.</li>
<li>GentooMuch is currently being developed on AMD64 systems but support for others will come very, very soon.
</li>
</ol>
</p>
<p>
I think this code generally represents best practices for maintaining multiple systems in everyone's favourite meta-distribution. Nothing is ever perfect and since upstream is a moving target, there will always be something to do. Not to mention that you can always find a list of best practices with conflicting advice: Choices were made. However, this toolkit is solid: Even when this thing was only half-built, working with Portage was already a saner experience than it had ever been beforehand.
</p>
