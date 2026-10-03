#!/usr/bin/python3

# Can be used for update to install over old.

from install_modules.c_configer import *

import sys, os, subprocess
import stat
from pathlib import Path
from datetime import datetime



# ++++++++++++++++++++++++++++++++++++++++++++
# Default values.
# Get all these from config.
# ++++++++++++++++++++++++++++++++++++++++++++


cc = c_configer('install.config')
fname_user_install_config = 'install_user.config'
if os.path.isfile(fname_user_install_config):
  cc.load(fname_user_install_config)
cc.parse_arguments(sys.argv)
cc.print_config()



os.chdir('../..')
sou = cc.install_dir+'/'
des = cc.install_location+'/'+cc.final_dir
# ief:  install excludes file
ief = cc.install_dir+'/install/install.excludes'
#

# print("install_dir: ", cc.install_dir)
# print("ief: ", ief)
# sys.exit(0)

cmd = ['rsync', '-avz', '--delete']
cmd += ['--exclude-from='+ief]
cmd += [sou, des]
rv = subprocess.call(cmd)
if rv != 0:
  print("Error.  rv != 0.")
  sys.exit(1)



os.chdir(cc.run_call_location)
# rcsl:  run call symlink
rcsl_target = Path(cc.install_location+'/'+cc.final_dir+'/start.sh')
rcsl_path   = Path(cc.run_call_location+'/'+cc.run_call)

print("rcsl_target: ", rcsl_target)
print("rcsl_path:   ", rcsl_path)


# if rcsl_path.exists():
# This only returns true if the link is not broken.

if os.path.lexists(rcsl_path):
  if not rcsl_path.is_symlink():
    print("Error.")
    print("  The run call already exists")
    print("  but it's not a symlink.")
    sys.exit(1)
  os.unlink( cc.run_call )

rcsl_path.symlink_to(rcsl_target)

# Write the install values used to install.log.
cc.save_config('install/install.log', 'log')
cc.save_config('install/install_final.config','final')

os.chdir( cc.install_location+'/'+cc.final_dir )
if not os.path.exists('start.sh'):
  progdir = os.getcwd()
  ou=''
  ou += '#!/bin/bash\n'
  ou += '\n'
  ou += 'pd='+progdir+'\n'
  ou += '\n'
  ou += 'source '+cc.venv_location
  ou += '/'+cc.venv_name+'/bin/activate\n'
  ou += '$pd/aamain.py\n'
  ou += 'deactivate\n'
  ou += '\n'
  fz=open('start.sh','w');
  fz.write(ou); fz.close()

# Want rwx r-x r-x
#      7   5   5
# r4 w2 x1.  7=4+2+1, 5=4+1.
os.chmod('start.sh', 0o755)

print("All done.")



