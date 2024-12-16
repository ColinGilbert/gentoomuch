#!/usr/bin/env python3

import re, os
from pathlib import Path
from .get_dockerized_profile_name import get_dockerized_profile_name


#Stuff all scripts here should use
debug				        	= True
output_path				    	= os.path.join(Path.home(), 'gentoomuch-data')
stages_path		            	= os.path.join(output_path, 'stages')
gpg_path				    	= os.path.join(output_path, 'gpg')
emergelogs_path             	= os.path.join(output_path, 'emerge.logs')
desired_stage_path		    	= os.path.join(output_path, 'desired_stage')
desired_profile_path	    	= os.path.join(output_path, 'desired_profile')
desired_packages_path	    	= os.path.join(output_path, 'desired_packages')
desired_hooks_path		    	= os.path.join(output_path, 'desired_hooks')
profiles_path                   = os.path.join(output_path, 'profiles')
kernels_out_path                = os.path.join(output_path, 'kernels')
# Portage-related
portage_output_path		    	= os.path.join(output_path, 'portage')
sets_output_path		    	= os.path.join(portage_output_path, 'sets')
patches_output_path             = os.path.join(portage_output_path, 'patches')
# Includes (immutable data)
includes_path			    	= './include'
global_config_path		    	= os.path.join(includes_path, 'portage.global')
# Config defines
config_path				    	= '/vagrant/config'
stage3_defines_path		    	= os.path.join(config_path, 'stage3.defines')
stage4_defines_path		    	= os.path.join(config_path, 'stage4.defines')
cpu_path				    	= os.path.join(config_path, 'cpu.defines')
pkgset_path				    	= os.path.join(config_path, 'package.sets')
local_config_basepath	        = os.path.join(config_path, 'portage.locals')
hooks_path				        = os.path.join(config_path, 'build.hooks')
kernel_configs_path				= os.path.join(config_path, 'kernel.configs')
saved_patches_path		        = os.path.join(config_path, 'user.patches')
# Environment settings (ie: Stuff you set and forget.)
env_settings_path               = os.path.join(config_path, 'env')
arch_config_path		        = os.path.join(env_settings_path, 'arch')
# These pertain to the stage signing.
digests_ext                     =".DIGESTS"
asc_ext			                = '.asc'
gentoo_signing_key		        = "0xBB572E0E2D182910"
gentoo_upstream_url             = "http://ftp-osl.osuosl.org/pub/gentoo/releases/"
# This is for the Docker tags that we access as we work.
image_tag_base			        = 'localhost:5000/gentoomuch-'
active_image_tag		        = image_tag_base + 'current:latest'
#profiles_amd64_dockerized	    =  ( get_dockerized_profile_name(p) for p in profiles_amd64 )
dockerized_username             = 'gentoomuch-user'
usage_str                       = "    gentoomuch "
# Patches
patches_export_mountpoint       = os.path.join('/mnt', 'patches')
kconfigs_mountpoint             = os.path.join('/mnt', 'kconfigs')
patches_workdir                 = os.path.join(output_path, 'patches.work')