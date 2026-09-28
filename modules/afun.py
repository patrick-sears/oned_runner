#!/usr/bin/env python3

import sys

def get_hex_str(hx):
  hhx = hx.hex()
  n_hx = len(hx)
  ou = ''
  for i in range(n_hx):
    ou += ' '+hhx[2*i:2*i+2]
  return ou[1:]


def timedelta_str(tdo):
  sec_tot = int( tdo.total_seconds() )
  mi_tot  = sec_tot // 60
  hr_tot  = mi_tot  // 60
  day_tot = hr_tot  // 24
  #
  day = day_tot
  hr  = hr_tot  - day_tot * 24
  mi  = mi_tot  - hr_tot  * 60
  sec = sec_tot - mi_tot  * 60
  #
  ou = ''
  ou += '{:2d}d'.format(day)
  ou += ' {:02d}'.format(hr)
  ou += ':{:02d}'.format(mi)
  ou += ':{:02d}'.format(sec)
  #
  return ou


def parse_ints(m):
  ms = m.strip()
  ll = (' '.join(ms.split())).split()
  ouints = []
  n_ll = len(ll)
  # for p in ll:
  for i in range(n_ll):
    p = ll[i]
    pp = p.split('-')
    n_pp = len(pp)
    if n_pp == 2:
      p0=int(pp[0]);  p1=int(pp[1]);
      if p1 < p0:
        print("Error.  p1 < p0.")
        print("  file:  afun.py.")
        print("  func:  parse_ints().")
        print("  input: ", ms)
        sys.exit(1)
      p1+=1;
      for j in range(p0, p1):
        ouints.append( j )
    elif n_pp == 1:
      ouints.append( int(p) )
    else:
      print("Error.  Bad n_pp.")
      print("  file:  afun.py.")
      print("  func:  parse_ints().")
      print("  input: ", ms)
      sys.exit(1)
    #
    #
  return ouints

