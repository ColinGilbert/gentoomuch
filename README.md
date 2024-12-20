<p>
STATUS: Currently updating it to work correctly after three years' hiatus

</p>
<h3>GentooMuch: Because something like this was bound to happen...</h3>

<h4>Intro:</h4>
<p>
I absolutely <i>fell in love</i> with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. The significant advantage of a tailored operating system is as things remain in harmony. However, unless carefully managed, a source-based distribution such as Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This toolkit provides automations to enable such careful management. Using Gentoomuch allows any user to be brave... If you use source control on the config directory, then congratulations: your builds are now reproducible. Gentoo and DevOps are coming closer together.
</p>
<p>
GentooMuch allows Gentoo users to reversibly experiment with unknown use-flag combinations and easily create patches for broken packages. GentooMuch allows long-time developers another means to orchestrate their own build processes. It gives sysadmins who must juggle entire networks a modern way to reduce technical debt. Using this tool is a rather civilized way of managing multiple Gentoo installations; it has very good amenities.
</p>
<h4>GentooMuch allows you manage an entire network's worth of Gentoo systems without fuss, while still being fun to use!</h4>
Gentoo Linux has been cast as intimidating and error-prone, and this toolkit aims to remove the bad by ensuring that all your builds are from a known state and by offering you an easy way to define and build multiple systems! We use Docker-Compose to maintain a clean working environment on every run. The software creates an optimized buildmaster directly from any of the publicly-available stage3s. However, this toolkit also keeps the best part of Gentoo; it is a <i>fun</i> little toolkit!
<p>
GentooMuch aims to to dovetail into the existing ecosystem by being very carefully designed for minimum intrusiveness: Due to being greatly inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to existing users. The tool also feels a bit like using the Docker command and that is no coincidence.
</p>
<h4>This tool is just made to be played with.</h4>
In fact, to setup, just download your stage3 and .asc, then call
<pre>gentoomuch bootstrap profile_name stage3-*.tar.xz</pre>
This creates an optimized builder. You then enter into an fresh sandbox environment with
<pre>gentoomuch freshroot</pre>
and start emerging packages right away! It'll keep the built ones so you won't have to recompile them from scratch again.
</p>
<p>
We support the important use-case of prepping and using patches when a package breaks; if upstream has a package broken on the minimalistic and marginally-supported libc you're using on your tricked-out system, and you need to quickly make it work, just go
<pre>gentoomuch patch prep</pre>
You work in the directory that gets automatically prepared for your convenience <pre>~/gentoomuch-data/patches</pre> and then you try compiling the patched package with
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
directory; the rest is either an executable file/deps, or documentation, or temporaries. A configuration called "gentoomuch/builder" exiusts. Modify it sparingly.
</li>
<li>Further documentation is in the config directory. These aforementioned folders are intended to be both part of our pipeline and as living, implicitly-tested documentation for anyone looking to get started.</li>
</ol>
<h4>What's the catch?</h4>
Nothing ever comes completely cost-free - If you are an existing (ie: skeptical) Gentoo user asking yourself whether or not this tool is worthwhile, I will be upfront about the limitations:
<ol>
<li>Portage hates not being in control of the kernel sources (especially when compiling/signing kernel modules), so we limit the user to a single version of gentoo-sources, which can be modified in gentoomuch/builder's local portage config files. Support for vanilla-sources and others is planned for a future release.</li>
<li>Your workflow will change a bit. Mostly it'll mean creating subdirectories for your sets of packages/flags and then defining your machines from these sets, instead of directly within /etc/portage, Also, you now access your build environments by using the freshroot command.</li>
<li>When building stage3 Docker images, GentooMuch keeps the tarball inside the image instead of deleting it as upstream does with theirs. This does entail an additional cost of 200-300MiB of space per profile you bootstrap on your local machine. However, you then benefit by completely avoiding the chicken-and-egg situation!</li>
<li>Bootstrapping dockerized images, epsecially for the first time, can take a while. This is because we do emerge --emptytree with ROOT=/mnt/gentoo which makes Portage re-emerge each package twice, once for / and once for /mnt/gentoo.</li>
</ol>
</p>
<p>
I think this code generally represents best practices for maintaining multiple systems in everyone's favourite meta-distribution. Nothing is ever perfect and since upstream is a moving target, there will always be something to do. Not to mention that you can always find a list of best practices with conflicting advice: Choices were made. However, this toolkit is solid: Even when this thing was only half-built, working with Portage was already a saner experience for me than it had ever been beforehand. I hope you find it useful too.
</p>
