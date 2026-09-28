#!/usr/bin/env python3

import sys
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
  def set_rchan(self, rchan):
    self.rchan = rchan
    self.n_rchan = len(rchan)
  def set_sola(self, sola):
    self.sola = sola
    #
    #
  def go_run(self, i_run, run_stime):
    imi     = self.imi
    rchan   = self.rchan
    n_rchan = self.n_rchan
    #
    fomb = "%Y-%m-%d %a %H:%M:%S"
    print("Starting run ", i_run)
    print("  ",run_stime.strftime(fomb))
    oulog = '!run_start ; '+str(i_run)+'\n'
    self.rlog.add(oulog)
    #
    # Sola:  Turn on ex light.
    self.sola.set_light_on()
    #
    for i in range(n_rchan):
      chani = rchan[i].chani
      print("Running channel ", chani)
      imi = rchan[i].go_run(imi)
    #
    # Sola:  Turn off ex light.
    self.sola.set_light_off()
    #
    self.imi = imi
    #
    oulog = '!run_end ; '+str(i_run)+'\n'
    self.rlog.add(oulog)
    self.rlog.save()
    #



