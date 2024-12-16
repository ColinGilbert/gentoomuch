In this folder are definitions for build-time hooks. This system is completely optional; you can generate proper stages without anything written here. The seven directories where you actually enter definitions are:

(Happens inside chroot)

- `unmerge`: A list of packages that need unmerging.
- `scripts:`: These scripts will be
- `services`: These services will be added to our base system, for a given runlevel. At present, only OpenRC is supported but SystemD is a possibility for the future.

(Happens outside chroot)

- `rm`: Removes individual files.
- `empty`: rm -rf's entire subdirectories, using root privileges.

Finally, in `tuple.defines` we assemble our subset of hooks and refer to that handle, instead of having to assemble a multipart list every time.

Notes:

- Hierachical/recursive definitions were strongly considered; I ultimately decided against them as we already get to use sets, and didn't want to duplicate the functionality. At some point this may change!
