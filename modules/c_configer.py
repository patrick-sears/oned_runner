#!/usr/bin/env python3

import sys, os
from datetime import datetime, timedelta

class c_configer:
  def __init__(self, fname=None):
    if fname != None:  self.load(fname)
    #
  def load(self, fname):
    f = open(fname)
    for l in f:
      l = l.strip()
      if len(l) == 0:  continue
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      # ll = ( ' '.join(l.split()) ).split()
      key = mm[0]
      if key == None:      pass
      elif key == '!schedule_tdo':  self.fread_schedule_tdo(f)
      elif key == '!run_mode':  self.run_mode = mm[1]
      elif key == '!chanset_file':  self.chanset_file = mm[1]
      elif key == '!chan_order':
          self.parse_chan_order( mm[1] )
      elif key == '!im_save_dir':  self.im_save_dir = mm[1]
      elif key == '!port_sola':  self.port_sola = mm[1]
      elif key == '!port_stage':  self.port_stage = mm[1]
      elif key == '!stage_units_per_mm':
            self.stage_units_per_mm = float(mm[1])
      elif key == '!stage_center_xyz':
        self.stage_center_x = float(mm[1])
        self.stage_center_y = float(mm[2])
        self.stage_center_z = float(mm[3])
      elif key == '!stage_limits':
        self.fread_stage_limits(f)
      elif key == '!xxx':  self.xxx = mm[1]
      elif key == '!xxx':  self.xxx = mm[1]
      else:
        print("Error in c_configer.  Unrecognized key.")
        print("  key: ", key)
        sys.exit(1)
    f.close()
    #
    self.pro1()
    #
  def fread_xxx(self, f):
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      # ll = ( ' '.join(l.split()) ).split()
      key = mm[0]
      if key == None:      pass
      elif key == '!xxx':  self.xxx = mm[1]
    #
  def fread_stage_limits(self, f):
    XYZ = 0
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      xyz = mm[0]
      #
      vv = [ float(mm[1]),  float(mm[2]) ]
      vv.sort()
      if xyz == 'x':
        self.stage_limit_x_lo = vv[0]
        self.stage_limit_x_hi = vv[1]
        XYZ |= 0x01
      elif xyz == 'y':
        self.stage_limit_y_lo = vv[0]
        self.stage_limit_y_hi = vv[1]
        XYZ |= 0x02
      elif xyz == 'z':
        self.stage_limit_z_lo = vv[0]
        self.stage_limit_z_hi = vv[1]
        XYZ |= 0x04
      else:
        print("Error.  Unrecognized xyz in config.")
        print("  stage_limits.")
        print("  xyz:  ", xyz)
        sys.exit(1)
      #
    #
    if XYZ != 0x07:
      print("Error.  Missing xyz from stage_limits.")
      print("  x: ", (XYZ & 0x01) > 0)
      print("  y: ", (XYZ & 0x02) > 0)
      print("  z: ", (XYZ & 0x04) > 0)
      sys.exit(1)
    #
    #
  def fread_schedule_tdo(self, f):
    #
    sched_t   = []
    tdx = []
    tdo = []
    t_cum = 0
    # foma = "%Y-%m-%d %H:%M:%S"
    for l in f:
      l = l.strip()
      if len(l) == 0:  break
      if l[0] == '#':  continue
      mm = [m.strip() for m in l.split(';')]
      # ll = ( ' '.join(l.split()) ).split()
      n = int( mm[0] )
      t = int( mm[1] )
      #
      for i in range(n):
        tdx.append( t )
        t_cum += t
        tt = timedelta(seconds=t_cum)
        tdo.append(tt)
    #
    self.schedule_tdx = tdx
    self.schedule_tdo = tdo
    n_run = len(tdo)
    print("n_run: ", n_run)
    #
    print("Run times from t0.")
    for i in range(n_run):
      print("  run["+str(i)+"]  ",tdo[i].total_seconds())
    print()
    #
  def parse_chan_order(self, m1):
    ll = ( ' '.join(m1.split()) ).split()
    self.chan_order = []
    for l in ll:
      self.chan_order.append( int(l) )
    #
  def pro1(self):
    rm = self.run_mode
    if rm != "serial" and rm != "simulation":
      print("Error.  Strange run_mode.")
      print("  run_mode: ", run_mode)
      sys.exit(1)
    #
    im_save_dir = self.im_save_dir
    if not os.path.exists(im_save_dir):
      os.mkdir(im_save_dir)
    #
    lisa = os.listdir(im_save_dir)
    if len(lisa) > 0:
      print("Error.")
      print("  im_save_dir is not empty.")
      sys.exit(1)
    #
    #
    #


