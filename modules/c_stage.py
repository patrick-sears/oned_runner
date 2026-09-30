#!/usr/bin/env python

import sys
import serial
# Requires pyserial

class c_stage:
  def __init__(self):
    pass
    #
  def set_run_mode(self, run_mode):
    self.run_mode = run_mode
  def set_port(self, port):
    self.port = port
  def set_stage_units_per_mm(self, stage_units_per_mm):
    self.stage_units_per_mm = stage_units_per_mm
  def set_stage_center_x(self, stage_center_x):
    self.stage_center_x = stage_center_x
  def set_stage_center_y(self, stage_center_y):
    self.stage_center_y = stage_center_y
  def set_stage_center_z(self, stage_center_z):
    self.stage_center_z = stage_center_z
    #
  def set_user_o_sx(self, user_o_sx):
    self.user_o_sx = user_o_sx
    # stage coords x pos for user origin.
  def set_user_o_sy(self, user_o_sy):
    self.user_o_sy = user_o_sy
  def set_user_o_sz(self, user_o_sz):
    self.user_o_sz = user_o_sz
    #
  def set_user_origin_to_stage_center(self):
    self.user_o_sx = self.stage_center_x
    self.user_o_sy = self.stage_center_y
    self.user_o_sz = self.stage_center_z
    #
  def set_stage_limits(self, xlo,xhi,ylo,yhi,zlo,zhi):
    self.stage_limit_x_lo = xlo;
    self.stage_limit_x_hi = xhi;
    self.stage_limit_y_lo = ylo;
    self.stage_limit_y_hi = yhi;
    self.stage_limit_z_lo = zlo;
    self.stage_limit_z_hi = zhi;
    #
  def is_in_limits_x(self,x):
    if x < self.stage_limit_x_lo:  return False
    if x > self.stage_limit_x_hi:  return False
    return True
  def is_in_limits_y(self,y):
    if y < self.stage_limit_y_lo:  return False
    if y > self.stage_limit_y_hi:  return False
    return True
  def is_in_limits_z(self,z):
    if z < self.stage_limit_z_lo:  return False
    if z > self.stage_limit_z_hi:  return False
    return True
  def is_in_limits_xy(self,x,y):
    if not self.is_in_limits_x(x):  return False
    if not self.is_in_limits_y(y):  return False
    return True
  def is_in_limits_xyz(self,x,y,z):
    if not self.is_in_limits_x(x):  return False
    if not self.is_in_limits_y(y):  return False
    if not self.is_in_limits_z(z):  return False
    return True
    #
  def get_stage_coords(self, ux,uy,uz):
    # Get stage coords from user coords.
    dsx = ux * self.stage_units_per_mm
    sx = self.user_o_sx - dsx
    #
    dsy = uy * self.stage_units_per_mm
    sy = self.user_o_sy + dsy
    #
    dsz = uz * self.stage_units_per_mm
    sz = self.user_o_sz - dsz
    return sx, sy, sz
    #
  def get_user_coords(self, sx,sy,sz):
    # Get user coords from stage coords.
    ssx = self.user_o_sx - sx
    ux = ssx / self.stage_units_per_mm
    #
    ssy = sy - self.user_o_sy
    uy = ssy / self.stage_units_per_mm
    #
    ssz = self.user_o_sz - sz
    uz = ssz / self.stage_units_per_mm
    return ux, uy, uz
    #
    #
  def init_serial(self):
    if self.run_mode != 'serial':
      print("c_stage:  Simulated init.")
      return
    #
    # 9600 8 N 1
    try:
      self.seri = serial.Serial(
        # port="/dev/prs_prior",
        port=self.port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,
        write_timeout=1,
        )
    except:
      print("c_stage:  Failed to open serial port.")
      sys.exit(1)
    #
  def cbuf(self):
    if self.run_mode != 'serial':
      print("c_stage:  Simulated cbuf().")
      return
    # Clear buffer.
    seri = self.seri
    while True:
      serda = seri.readline()
      slen = len(serda)
      if len == 0:  break
      # dade = serda.decode("Ascii")
      # print("  serda: ", dae)
    #
  def sread_user_xyz(self):
    sx,sy,sz = self.sread_stage_xyz()
    ux,uy,uz = self.get_user_coords(sx,sy,sz)
    return ux,uy,uz
  def sread_stage_xyz(self):
    # sread:  serial read.
    if self.run_mode != 'serial':
      print("c_stage:  Simulated sread_stage_xyz().")
      return 57000,37500,15000
    #
    seri = self.seri
    self.cbuf()
    ouline = 'p\r\n'
    send = bytes(ouline.encode())
    seri.write(send)
    serda = seri.readline()
    l = serda.decode("Ascii")
    ll = l.split(',')
    x=int(ll[0]); y=int(ll[1]); z=int(ll[z]);
    return [x,y,z]
    #
  def go_user_xyz(self, ux, uy, uz):
    sx,sy,sz = self.get_stage_coords(ux,uy,uz)
    self.go_stage_xyz(sx, sy, sz)
  def go_stage_xyz(self, x,y,z):
    if not self.is_in_limits_xyz(x,y,z):
      print("Error.  Outside stage limits.")
      print("  file:  c_stage.py")
      print("  func:  go_stage_xyz().")
      sys.exit(1)
    if self.run_mode != 'serial':
      # print("c_stage:  Simulated stage_xyz().")
      return
    #
    seri = self.seri
    ou = 'g'
    ou += ' {:0d}'.format( x )
    ou += ' {:0d}'.format( y )
    ou += ' {:0d}'.format( z )
    ou += '\r\n'
    send = bytes( ou.encode() )
    seri.write( send )
    #
    # When done, it should return 'R'.
    serda = seri.readline()
    dade = serda.decode("Ascii")
    dade = date.strip() # Not sure if this is needed.
    if dade != 'R':
      print("Warning.  Expected 'R'.")
      print("  Got:  ", dade)
      print("  File:  c_stage.py.")
      print("  Function stage_xyz().")
    #
  def go_user_xy(self, ux, uy):
    sx,sy,sz = self.get_stage_coords(ux,uy,0)
    self.go_stage_xy(sx, sy)
  def go_stage_xy(self, x,y):
    if not self.is_in_limits_xy(x,y):
      print("Error.  Outside stage limits.")
      print("  file:  c_stage.py")
      print("  func:  go_stage_xy().")
      sys.exit(1)
    if self.run_mode != 'serial':
      # print("c_stage:  Simulated go_p3().")
      return
    #
    seri = self.seri
    ou = 'g'
    ou += ' {:0d}'.format( x )
    ou += ' {:0d}'.format( y )
    ou += '\r\n'
    send = bytes( ou.encode() )
    seri.write( send )
    #
    # When done, it should return 'R'.
    serda = seri.readline()
    dade = serda.decode("Ascii")
    dade = date.strip() # Not sure if this is needed.
    if dade != 'R':
      print("Warning.  Expected 'R'.")
      print("  Got:  ", dade)
      print("  File:  c_stage.py.")
      print("  Function go_stage_xy().")
    #
  def reset_z0_to_current_stage_position(self):
    if self.run_mode != 'serial':
      return
    #
    seri = self.seri
    ou = 'pz 0'
    ou += '\r\n'
    send = bytes( ou.encode() )
    seri.write( send )
    # When done, it should return '0'.
    serda = seri.readline()
    dade = serda.decode("Ascii")
    dade = date.strip() # Not sure if this is needed.
    if dade != '0':
      print("Warning.  Expected '0'.")
      print("  Got:  ", dade)
      print("  File:  c_stage.py.")
      print("  Func:  c_reset_z0_to_current_stage_position.py.")
    #
    #





