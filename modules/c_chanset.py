#!/usr/bin/env python3

# Only for loading channels.
# Not for the actual runs.
#
# Contains all the channels in the
# capillary holder or microfluidic plate.

from modules.afun import parse_ints
from modules.c_channel import *

import sys

class c_chanset:
  def __init__(self):
    pass
    #
  def set_stage(self, stage):
    self.stage = stage
  def set_run_mode(self, run_mode):
    self.run_mode = run_mode
  def set_chan_order(self, chan_order):
    self.chan_order = chan_order
    self.n_rchan = len(chan_order)
    #
  def load(self, fname):
    f = open(fname)
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      key = mm[0]
      if key=='!channels':
        self.fread_channels(f)
      elif key=='!point_sequence':
          self.fread_point_sequence(f)
      elif key=='!camera_subarray':
          self.fread_camera_subarray(f)
      elif key=='!fidu':
        self.fread_fidu(f)
      elif key=='!specs':
        # Ignore specs.
        for l in f:
          if l.strip() == 0:  break
      elif key=='!xxx':  self.fread_xxx(f)
      elif key=='!xxx':  self.fread_xxx(f)
      else:
        print("Error.  Unrecognized key.")
        print("  key:  ", key)
        print("  file: ", fname)
        sys.exit(1)
      #
    f.close()
    #
  def fread_fidu(self, f):
    self.fidu_name = []
    self.fidu_x = []
    self.fidu_y = []
    self.fidu_z = []
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      self.fidu_name.append( mm[0] )
      self.fidu_x.append( float(mm[1]) )
      self.fidu_y.append( float(mm[2]) )
      self.fidu_z.append( float(mm[3]) )
    #
    self.n_fidu = len(self.fidu_name)
    #
  def set_run_mode_in_channels(self):
    run_mode = self.run_mode
    for i in range(self.n_chan):
      self.chan[i].set_run_mode(run_mode)
    #
  def pro1(self):
    for i in range(self.n_chan):
      self.chan[i].pro1()
    #
  def fread_xxx(self, f):
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      # ll = (' '.join(l.split())).split()
    #
  def fread_channels(self, f):
    self.chan = []
    ii = -1
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      ii += 1
      jj = int( mm[0] )
      if ii != jj:
        print("Error.  ii != jj.")
        print("  ii, jj: ", ii, jj)
        sys.exit(1)
      uchan = c_channel()
      uchan.parse1( mm )
      self.chan.append( uchan )
    #
    self.n_chan = len(self.chan)
    #
  def fread_point_sequence(self, f):
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      m_start = float(mm[0]);
      m_end   = float(mm[1]);
      dL_step = float(mm[2]);
      uchans = parse_ints(mm[3])
      for uc in uchans:
        if uc < 0 or uc >= self.n_chan:
          print("Error.  uc out of range.")
          print("  uc: ", uc)
          print("  file:  c_chanset.py.")
          print("  func:  fread_point_sequence().")
          sys.exit(1)
        if self.chan[uc].m_start != None:
          print("Error.  Duplicate assignment.")
          print("  uc: ", uc)
          print("  file:  c_chanset.py.")
          print("  func:  fread_point_sequence().")
          sys.exit(1)
        self.chan[uc].set_m_start( m_start   )
        self.chan[uc].set_m_end(   m_end     )
        self.chan[uc].set_dL_step( dL_step   )
    #
    for i in range(self.n_chan):
      if self.chan[i].m_start == None:
        print("Error.")
        print("  - A channel is missing")
        print("    the point sequence.")
        print("  chan i: ", i)
        print("  file:  c_chanset.py.")
        print("  func:  fread_point_sequence().")
        sys.exit(1)
    #
  def fread_camera_subarray(self, f):
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      x1=int(mm[0]);  y1=int(mm[1]);
      x2=int(mm[2]);  y2=int(mm[3]);
      uchans = parse_ints(mm[4])
      for uc in uchans:
        if uc < 0 or uc >= self.n_chan:
          print("Error.  uc out of range.")
          print("  uc: ", uc)
          print("  file:  c_chanset.py.")
          print("  func:  fread_camera_subarray().")
          sys.exit(1)
        if self.chan[uc].csa_x1 != None:
          print("Error.  Duplicate assignment.")
          print("  uc: ", uc)
          print("  file:  c_chanset.py.")
          print("  func:  fread_camera_subarray().")
          sys.exit(1)
        # csa:  camera sub-array.
        self.chan[uc].set_csa_x1(x1)
        self.chan[uc].set_csa_y1(y1)
        self.chan[uc].set_csa_x2(x2)
        self.chan[uc].set_csa_y2(y2)
    #
    for i in range(self.n_chan):
      if self.chan[i].csa_x1 == None:
        print("Error.")
        print("  - A channel is missing")
        print("    the camera subarray.")
        print("  chan i: ", i)
        print("  file:  c_chanset.py.")
        print("  func:  fread_camera_subarray().")
        sys.exit(1)
    #
    #
  def reset_user_origin_with_fidu0(self):
    # That is, set where in stage coordinates
    # the user origin is located.
    f0x = self.fidu_x[0]
    f0y = self.fidu_y[0]
    self.stage.go_user_xy(f0x,f0y);
    print("Resetting location of user origin")
    print("  in stage coordinate system")
    print("  using fiducial point 0.")
    print("  Adjust position of fidu[0],")
    print("  then hit enter.")
    uin = input("  >> ")
    # Don't bother checking.
    sx,sy,sz = self.stage.sread_stage_xyz()
    if self.run_mode != 'serial':  return
    self.stage.set_user_o_sx( sx )
    self.stage.set_user_o_sy( sy )
    self.stage.set_user_o_sz( sz )
    #
  def reset_edges(self):
    order = self.chan_order
    n_rchan = self.n_rchan
    ok = True
    #
    # First reset user origin using fidu[0].
    # Using only fidu[0] for now.
    self.reset_user_origin_with_fidu0()
    #
    print("Reset capillary ends for each")
    print("  capillary that will be used.")
    for i in range(n_rchan):
      ii = order[i]
      rv = self.chan[ii].reset_edges()
      if rv != 0:
        ok = False
        break
    if ok:  return 0
    return 1
    #
  def save_channels_1a(self, fzname):
    ou = ''
    ou += '#\n'
    ou += '\n'
    ou += '# Units:  mm.\n'
    ou += '\n'
    ou += '!channels\n'
    ou += '# i ;; bx        ; by        ; bz        ;; cx        ; cy        ; cz\n'
    for i in range(self.n_chan):
      bx,by,bz = self.chan[i].get_pos_bxyz()
      cx,cy,cz = self.chan[i].get_pos_cxyz()
      ou += '{:3d}'.format(i)
      ou += ' ;; {:9.3f}'.format(bx)
      ou += ' ; {:9.3f}'.format(by)
      ou += ' ; {:9.3f}'.format(bz)
      ou += ' ;; {:9.3f}'.format(cx)
      ou += ' ; {:9.3f}'.format(cy)
      ou += ' ; {:9.3f}'.format(cz)
      ou += '\n'
    #
    ou += '\n'
    ou += '!point_sequence\n'
    ou += '# m_start ; m_end  ; dL_step ; channels\n'
    for i in range(self.n_chan):
      m_start   = self.chan[i].m_start
      m_end   = self.chan[i].m_end
      dL_step = self.chan[i].dL_step
      #
      ou += '{:7.1f}'.format(m_start)
      ou += ' ; {:6.1f}'.format(m_end)
      ou += ' ; {:7.3f}'.format(dL_step)
      ou += ' ; {:6d}'.format(i)
      ou += '\n'
    #
    ou += '\n'
    ou += '!camera_subarrray\n'
    ou += '# x1   ; y1     ; x2     ; y2     ; channels\n'
    for i in range(self.n_chan):
      x1=self.chan[i].csa_x1;
      y1=self.chan[i].csa_y1;
      x2=self.chan[i].csa_x2;
      y2=self.chan[i].csa_y2;
      #
      ou += '{:6d}'.format(x1)
      ou += ' ; {:6d}'.format(y1)
      ou += ' ; {:6d}'.format(x2)
      ou += ' ; {:6d}'.format(y2)
      ou += ' ; {:6d}'.format(i)
      ou += '\n'
    #
    ou += '\n'
    ou += '# The specs section is not loaded.\n'
    ou += '# Actual length will depend on camera FOV'
    ou += '# and n_im.\n'
    ou += '!specs\n'
    ou += '# chani ; n_im ; Len_sweep\n'
    for i in range(self.n_chan):
      m_start     = self.chan[i].m_start
      m_end     = self.chan[i].m_end
      dL_step   = self.chan[i].dL_step
      n_im      = self.chan[i].n_im
      Len_sweep = self.chan[i].Len_sweep
      #
      ou += '{:7d}'.format(i)
      ou += ' ; {:4d}'.format( n_im )
      ou += ' ; {:7.3f}'.format( Len_sweep )
      ou += '\n'
      #
    #
    ou += '\n'
    ou += '\n'
    #
    fz=open(fzname,'w');
    fz.write(ou);  fz.close();
    #
  def save_channels_1b(self, fzname):
    order = self.chan_order
    n_rchan = self.n_rchan
    #
    ou = ''
    ou += '#\n'
    ou += '\n'
    ou += '# Units:  mm.\n'
    ou += '# Only running channels are listed.\n'
    ou += '# Channels listed in run order.\n'
    #
    ou += '\n'
    for i in range(n_rchan):
      ii = order[i]
      ou += self.chan[ii].gou_1a()
    ou += '\n'
    #
    fz=open(fzname,'w');
    fz.write(ou);  fz.close();


