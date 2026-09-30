#!/usr/bin/env python3

from modules.afun import timedelta_str
from modules.c_configer import *
from modules.c_stage import *
from modules.c_sola import *
from modules.c_camera import *
from modules.c_channel import *
from modules.c_chanset import *
from modules.c_runner import *
from modules.c_run_log import *


import sys
import time
from datetime import datetime

foma = "%Y-%m-%d %H:%M:%S"
fomb = "%Y-%m-%d %a %H:%M:%S"

cc = c_configer('config')

rlog = c_run_log()


sola = c_sola()
sola.set_run_mode(cc.run_mode)
sola.set_port(cc.port_sola)
sola.init_serial()

stage = c_stage()
stage.set_run_mode(cc.run_mode)
stage.set_port(cc.port_stage)
# ^^^^
stage.set_stage_units_per_mm(cc.stage_units_per_mm)
stage.set_stage_center_x(cc.stage_center_x)
stage.set_stage_center_y(cc.stage_center_y)
stage.set_stage_center_z(cc.stage_center_z)
stage.set_stage_limits( cc.stage_limit_x_lo,
                        cc.stage_limit_x_hi,
                        cc.stage_limit_y_lo,
                        cc.stage_limit_y_hi,
                        cc.stage_limit_z_lo,
                        cc.stage_limit_z_hi
                        )
stage.set_user_origin_to_stage_center()
# ^^^^
stage.init_serial()


camera = c_camera()
camera.set_run_mode(cc.run_mode)
camera.set_im_save_dir(cc.im_save_dir)
camera.init_serial()

chanset = c_chanset()
chanset.set_run_mode(cc.run_mode)
chanset.set_stage( stage )
chanset.load(cc.chanset_file)
chanset.set_run_mode_in_channels()
chanset.pro1()
chanset.save_channels_1a('z1a_chanset.data')


# n_rchan, number of channels that will be run.
# As opposed to total number in holder.
n_rchan = len(cc.chan_order)
rchan = []
for i in range(n_rchan):
  ii = cc.chan_order[i]
  if ii < 0 >= chanset.n_chan:
    print("Error.  ii out of range.")
    print("  ii: ", ii)
    sys.exit(1)
  rchan.append( chanset.chan[ii] )
  chanset.chan[ii].set_is_runner(True)
  chanset.chan[ii].set_order_i(i)

for i in range(n_rchan):
  rchan[i].set_rlog(rlog)
  rchan[i].set_stage(stage) # Prior stage
  rchan[i].set_camera(camera) # Basler camera

chanset.set_chan_order(cc.chan_order)
chanset.save_channels_1b('z1b_chanset.data')

print("Reset the z level to zero.")
print("  Focus on the channel or membrane.")
uin = input("  Then print enter. >> ")
# Ignore input.
stage.reset_z0_to_current_stage_position()


print()
print("Resetting origin using fiducial point 0.")
chanset.reset_user_origin_with_fidu0()

# I'm not sure this is where I want this.
# But note that it needs to come after setting
# the channel orders.
print()
print("Resetting edges.")
print("  Using only runner channels, in run order.")
rv = chanset.reset_edges()
if rv != 0:
  print("Program exit due to exit from reset_edges().")
  sys.exit(0)
chanset.pro1()  # Is this right?

# Save new edges after reset edges.
chanset.save_channels_1a('z2a_chanset.data')
chanset.save_channels_1b('z2b_chanset.data')
chanset.save_channels_1c('z2c_chanset_stage.data')

chanset.check_in_stage_limits()
# Exits with error if some points are
# not within stage limits.
# Checks runner channels, points b and c.

sched_tdx = cc.schedule_tdx
sched_tdo = cc.schedule_tdo
n_run = len(sched_tdo)

runner = c_runner()
runner.set_cc(cc)
runner.set_rlog(rlog)
runner.set_sola(sola) # sola seria
runner.set_rchan(rchan)


print()
print('Press enter to start, x to exit.')
print('  *** Remember to switch optical path')
print('      from oculars to camera.')
uin = input('  >> ')
if uin != '':
  print("Early exit.")
  sys.exit(0)

schedule = []
now = datetime.now()
for i in range(n_run):
  schedule.append(now + sched_tdo[i])


rlog.add("\n\n# _____________________________\n")
rlog.add('!new_run_set\n')
rlog.add('!stime ; '+now.strftime(fomb)+'\n')
rlog.add('\n')
rlog.save()

ou = ''
ou += '#\n'
ou += '!schedule\n'
ou += '# run ; dt (s)  ; t from start    ; start time\n'
for i in range(n_run):
  ou += '{:5d}'.format(i)
  ou += ' ; {:6d}'.format( sched_tdx[i] )
  ou += ' ; '+timedelta_str( sched_tdo[i] )
  ou += ' ; '+schedule[i].strftime(fomb)
  ou += '\n'
ou += '\n'
fz = open("z3a_schedule.data",'w')
fz.write(ou);  fz.close()

def uc_green(s):
  x     = '\033[0m'
  green = '\033[92m'
  return green+s+x

waiting_mark = uc_green('====================================')

i_run = 0
nex_t = schedule[0]
show_header = True
try:
  sola.set_intensity_50()
  #
  print()
  print("Schedule running...")
  while True:
    if show_header:
      print()
      print(waiting_mark)
      print("Waiting to start run ", i_run, "...")
      print("  Next run: ", nex_t.strftime(fomb))
      show_header = False
    #
    now = datetime.now()
    if now < nex_t:
      time.sleep(0.1)
      continue
    #
    runner.go_run(i_run, now)
    #
    # Prep for next run.
    show_header = True
    i_run += 1
    if i_run == n_run:  break
    else:               nex_t = schedule[i_run]
    #
  #
  #
except KeyboardInterrupt:
  print("Ctrl+C received. Stopping...")
  rlog.add('Ctrl-c received.\n')
  rlog.save()
finally:
  # Attempt to turn off on Ctrl+C
  # or a Python exception.
  sola.set_light_off()



rlog.add('Normal exit.\n')
rlog.save()




