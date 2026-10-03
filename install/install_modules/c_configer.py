#!/usr/bin/python3

from install_modules.afun import get_true_false_str
from install_modules.afun import get_str_of_true_false

import sys, os, subprocess
from pathlib import Path
from datetime import datetime




# ============================================
# Read config.
class c_configer:
  def __init__(self, fname=None):
    os.chdir('..')
    self.install_dir = Path.cwd().resolve().name
    os.chdir('install')
    if fname != None:  self.load(fname)
    #
  def load(self, fname):
    f = open('install.config')
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      if key == '!install_location':
        self.install_location = mm[1]
      elif key == '!final_dir': self.final_dir = mm[1]
      elif key == '!run_call_location': 
        self.run_call_location = mm[1]
      elif key == '!run_call': self.run_call = mm[1]
      elif key == '!user_config': self.user_config = mm[1]
      elif key == '!venv_name': self.venv_name = mm[1]
      elif key == '!venv_location': self.venv_location = mm[1]
      elif key == '!xxx': self.xxx = mm[1]
      elif key == '!xxx': self.xxx = mm[1]
      else:
        print("Error.")
        print("  Unrecognized key in install.config.")
        print("  key:  ", key)
        sys.exit(1)
    f.close()
    #
  def parse_arguments(self, arg):
    n_arg = len(arg)
    args_good = True
    ii = 1
    while ii < n_arg:
      if arg[ii] == '--install_location':
        if ii == n_arg:
          args_good = False
          break
        ii += 1
        self.install_location = arg[ii]
      elif arg[ii] == '--final_dir':
        if ii == n_arg:
          args_good = False
          break
        ii += 1
        self.final_dir = arg[ii]
      elif arg[ii] == '--run_call_location':
        if ii == n_arg:
          args_good = False
          break
        ii += 1
        self.run_call_location = arg[ii]
      elif arg[ii] == '--run_call':
        if ii == n_arg:
          args_good = False
          break
        ii += 1
        self.run_call = arg[ii]
      elif arg[ii] == '--user_config':
        if ii == n_arg:
          args_good = False
          break
        ii += 1
        self.user_config = arg[ii]
      else:
        args_good = False
        break
      # -------
      ii += 1
    #
    if not args_good:
      print("Error.  Reading install arguments.")
      sys.exit(1)
    #
    #
  def print_config(self):
    print("Final config values.")
    print("  install_dir ; ", self.install_dir)
    print("  install_location  ; ", self.install_location)
    print("  final_dir         ; ", self.final_dir)
    print("  run_call_location ; ", self.run_call_location)
    print("  run_call          ; ", self.run_call)
    print("  user_config       ; ", self.user_config)
    #
  def save_config(self, fzname, outype):
    fuzname = self.install_location+'/'+self.final_dir+'/'+fzname
    fom = '%Y-%m-%d %a %H:%M:%S'
    stime = datetime.now().strftime(fom)
    # def get_str_of_true_false(v):
    ou = ''
    if not os.path.exists(fuzname): ou += '#\n'
    ou += '\n'
    ou += '# ________________________________\n'
    ou += '# '+stime+'\n'
    ou += '!install_location  ; '+self.install_location+'\n'
    ou += '!final_dir         ; '+self.final_dir+'\n'
    ou += '!run_call_location ; '+self.run_call_location+'\n'
    ou += '!run_call          ; '+self.run_call+'\n'
    ou += '!user_config       ; '+self.user_config+'\n'
    ou += '\n'
    if outype == 'log':
      fz = open(fuzname,'a')
    elif outype == 'final':
      fz = open(fuzname,'w')
    else:
      print("Error.  Unrecognized outype.")
      sys.exit(1)
    fz.write(ou);  fz.close()
# ============================================




