#!/usr/bin/env python3


class c_run_log:
  def __init__(self):
    self.oulog = ''
    self.log_fname = 'zx-run.log'
    pass
  def add(self, ou):
    self.oulog += ou
  def save(self):
    fz = open(self.log_fname,'a')
    fz.write(self.oulog)
    fz.close()
    self.oulog = ''



