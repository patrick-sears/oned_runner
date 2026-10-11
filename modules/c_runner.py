#!/usr/bin/env python3

import sys, os
from datetime import datetime

class c_runner:
  def __init__(self):
    self.imi = 0
    pass
    #
  def set_cc(self, cc):
    self.cc = cc
  def set_rlog(self, rlog):
    self.rlog = rlog
  def set_im_save_dir(self, im_save_dir):
    self.im_save_dir = im_save_dir
  def set_rchan(self, rchan):
    self.rchan = rchan
    self.n_rchan = len(rchan)
  def set_sola(self, sola):
    self.sola = sola
    #
    #
  def go_run(self, i_pass, run_stime):
    imi     = self.imi
    rchan   = self.rchan
    n_rchan = self.n_rchan
    #
    fomb = "%Y-%m-%d %a %H:%M:%S"
    print("Starting pass ", i_pass)
    print("  ",run_stime.strftime(fomb))
    oulog = '!pass_start ; '+str(i_pass)+'\n'
    self.rlog.add(oulog)
    #
    # Sola:  Turn on ex light.
    self.sola.set_light_on()
    #
    oudir = []
    for i in range(n_rchan):
      oud = self.im_save_dir
      oud += 'pass{:03d}'.format(i_pass)
      oud += '-rc{:02d}/'.format(i)
      os.mkdir(oud)
      oudir.append(oud)
    #
    for i in range(n_rchan):
      chani = rchan[i].chani
      print("Running channel ", chani)
      # imi = rchan[i].go_run(imi)
      rchan[i].go_run(oudir[i])
    #
    # Sola:  Turn off ex light.
    self.sola.set_light_off()
    #
    self.imi = imi
    #
    oulog = '!pass_end ; '+str(i_pass)+'\n'
    self.rlog.add(oulog)
    self.rlog.save()
    #



