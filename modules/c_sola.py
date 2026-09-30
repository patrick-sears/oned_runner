#!/usr/bin/env python3

from modules.afun import get_hex_str

import sys
import serial
# Requires pyserial

class c_sola:
  def __init__(self):
    # SOLA initialization commands. Needed after power on/off.
    self.init_sola = [
      [0x57, 0x02, 0xFF, 0x50],
      [0x57, 0x03, 0xFD, 0x50],
      ]
    #
    # SOLA light on and off commands
    self.light_on  = [0x4f, 0x7d, 0x50]
    self.light_off = [0x4f, 0x7f, 0x50]
    #
    # SOLA light power level command
    self.intensity_max = [0x53, 0x46, 0x02, 0x01, 0x00, 0x50]
    self.intensity_min = [0x53, 0x46, 0x02, 0x01, 0xFF, 0x50]
    self.intensity_50  = [0x53, 0x46, 0x02, 0x01, 0x80, 0x50] # 50%
    #
  def set_run_mode(self, run_mode):
    self.run_mode = run_mode
  def set_port(self, port):
    self.port = port
    #
    #
  def init_serial(self):
    if self.run_mode != 'serial':
      print("c_sola:  Simulated init.")
      return
    #
    init_sola = self.init_sola
    light_on  = self.light_on
    light_off = self.light_off
    #
    # Input port as the serial ID.
    # Plan:  Use udev rules to create /dev/prs_sola.
    seri = None
    try:
      seri = serial.Serial(
        # port="/dev/prs_sola",
        port=self.port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,
        write_timeout=1,
        )
    except:
      print("c_sola:  Failed to open serial port.")
      sys.exit(1)
    #
    try:
      # for command in init_sola:  seri.write(command)
      print("DDD try init_sola[0].")
      seri.write( init_sola[0] )
      seri.flush()
      #
      print("DDD try init_sola[1].")
      seri.write( init_sola[1] )
      seri.flush()
      #
      print("DDD try light_off.")
      seri.write(light_off)
      seri.flush()
      #
      print("DDD Done init sola.")
    except:
      print("Failed init_sola.")
      sys.exit(1)
    #
    self.seri = seri
    #
    #
  def set_intensity_50(self):
    if self.run_mode != 'serial':
      send = get_hex_str(self.intensity_50)
      print()
      print("sim set_intensity_50()")
      print("  Write: ", send)
      return
    #
    seri = self.seri
    intensity_50 = self.intensity_50
    try:
      seri.write(intensity_50)
    except:
      print("Failed write.  intensity_50.")
      sys.exit(1)
    #
  def set_light_off(self):
    if self.run_mode != 'serial':
      send = get_hex_str(self.light_off)
      print("sim set_light_off()")
      print("  Write: ", send)
      return
    #
    try:
      self.seri.write(self.light_off)
      self.seri.flush()
    except:
      print("Error.  Bad write.")
      print("  set_light_off().")
      sys.exit(1)
    #
    #
    #
  def set_light_on(self):
    if self.run_mode != 'serial':
      send = get_hex_str(self.light_on)
      print()
      print("sim set_light_on()")
      print("  Write: ", send)
      return
    #
    try:
      self.seri.write(self.light_on)
      self.seri.flush()
    except:
      print("Error.  Bad write.")
      print("  set_light_on().")
      sys.exit(1)
    #



