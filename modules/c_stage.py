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
    #
  def init_serial(self):
    if self.run_mode != 'serial':
      print("c_stage:  Simulated init.")
      return
    #
    # 9600 8 N 1
    try:
      seri = serial.Serial(
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
  def get_p(self):
    if self.run_mode != 'serial':
      print("c_stage:  Simulated get_p().")
      return [100,101,102]
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
  def go_p3(self, x,y,z):
    if self.run_mode != 'serial':
      # print("c_stage:  Simulated go_p3().")
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
      print("  Function go_p3().")





