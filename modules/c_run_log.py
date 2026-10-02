#!/usr/bin/env python3


class c_run_log:
  def __init__(self):
    self.oulog = ''
    #
  def set_dz_run(self, dz_run):
    self.dz_run = dz_run
    self.log_fname = dz_run+'run.log'
    #
  def add(self, ou):
    self.oulog += ou
  def save(self):
    fz = open(self.log_fname,'a')
    fz.write(self.oulog)
    fz.close()
    self.oulog = ''



