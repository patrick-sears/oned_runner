#!/usr/bin/env python3

# See main_mpanther_2026/ comp--mpanther_OS1/
# 0915v10a--mpanther_os1_basler_pylon/

import sys
from pypylon import pylon
import cv2


class c_camera:
  def __init__(self):
    pass
    #
  def set_run_mode(self, run_mode):
    self.run_mode = run_mode
  def set_im_save_dir(self, im_save_dir):
    self.im_save_dir = im_save_dir
    #
  def init_serial(self):
    if self.run_mode != 'serial':
      print("c_camera:  Simulated init_serial().")
      return
    #
    factory = pylon.TlFactory.GetInstance()
    devices = factory.EnumerateDevices()
    n_devices = len(devices)
    if n_devices != 1:
      print("Error.  n_devices != 1.")
      print("  n_devices: ", n_devices)
      sys.exit(1)
    #
    # camd:  camera device
    de0 = devices[0]
    self.camd = devices[0]
    self.friendly_name = de0.GetFriendlyName()
    self.full_name = de0.GetFullName()
    self.serial_num = de0.GetSerialNumber()
    print("c_camera.")
    print("  friendly_name:  ", self.friendly_name)
    print("  serial_num:     ", self.serial_num)
    #
    # cama:  camera attachement
    self.cama = pylon.InstantCamera()
    self.cama.Attach(factory.CreateFirstDevice())
    #
  def take_image(self, imi):
    if self.run_mode != 'serial':
      # print("c_camera:  Simulated init.")
      ### # -----------------------
      ### # Used for testing during initial development.
      ### # No longer needed.
      ### imfuz = self.im_save_dir
      ### imfuz += '/im{:04d}.data'.format(imi)
      ### ou = 'Image {:04d}\n'.format(imi)
      ### with open(imfuz,'w') as f: f.write(ou)
      ### # -----------------------
      return
    #
    imfuz = self.im_save_dir
    imfuz += '/im{:04d}.png'.format(imi)
    #
    # Shouldn't this go in init_serial()?
    cama = self.cama
    #
    # Some of these values should be set
    # up somewhere else and should be ste
    # up per channel.
    # So each channel would first call
    # some kind of a setup_sweep() function.
    cetype = cama.PiselFromat.Value
    exauto = cama.ExposureAuto.Value
    extime = cama.ExposureTime.Value
    #
    cama.ExposureTime.Value = 100.0
    #
    timeout_ms = 2000;
    # If 2s pass, there is no result.
    #
    cama.Open()
    cama.StartGrabbing(1) # Grab 1 image.
    grab = cam.RetrieveResult( timeout_ms,
                pylon.TimeoutHandling_Return
                )
    #
    if not grab.GrabSucceeded():
      cama.Close()
      print("Error.  Grab did not succeed.")
      sys.exit(1)
    #
    ima = grab.GetArray()
    # ima is a numpy array.
    # print('ima shape: ', ima.shape)
    element_type = ima.dtype
    #
    # Save the image.
    cv2.imwrite(imfuz, ima)
    #
    cam.Close()
    #



