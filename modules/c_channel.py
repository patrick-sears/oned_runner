#!/usr/bin/env python3

from math import hypot

class c_channel:
  def __init__(self):
    # csa:  camera sub-array
    self.m_start  = None
    self.csa_x1 = None
    self.is_runner = False
    pass
    #
  def set_is_runner(self, is_runner):
    self.is_runner = is_runner
  def set_run_mode(self, run_mode):
    self.run_mode = run_mode
  def set_rlog(self, rlog):
    self.rlog = rlog
  def set_order_i(self, order_i):
    self.order_i = order_i
  def set_m_start(self, m_start):
    self.m_start = m_start
  def set_m_end(self, m_end):
    self.m_end = m_end
  def set_dL_step(self, dL_step):
    self.dL_step = dL_step
  def set_csa_x1(self, csa_x1):
    self.csa_x1 = csa_x1
  def set_csa_y1(self, csa_y1):
    self.csa_y1 = csa_y1
  def set_csa_x2(self, csa_x2):
    self.csa_x2 = csa_x2
  def set_csa_y2(self, csa_y2):
    self.csa_y2 = csa_y2
    #
  def set_stage(self, stage):
    self.stage = stage
  def set_camera(self, camera):
    self.camera = camera
    #
  def get_pos_bxyz(self):
    return self.pos_bx, self.pos_by, self.pos_bz
  def get_pos_cxyz(self):
    return self.pos_cx, self.pos_cy, self.pos_cz
    #
  def check_in_stage_limits(self):
    # Check points b and c.  Assume others in limits.
    stage=self.stage
    bx=self.pos_bx;  by=self.pos_by;  bz=self.pos_bz;
    cx=self.pos_cx;  cy=self.pos_cy;  cz=self.pos_cz;
    #
    sx,sy,sz = stage.get_stage_coords(bx,by,bz)
    if not stage.is_in_limits_xyz(sx,sy,sz):
      print("Error.  Out of stage limits.")
      print("  chani: ", self.chani)
      print("  bx by bz: ", bx, by, bz)
      print("  stage: ", sx, sy, sz)
      sys.exit(1)
    #
    sx,sy,sz = stage.get_stage_coords(cx,cy,cz)
    if not stage.is_in_limits_xyz(sx,sy,sz):
      print("Error.  Out of stage limits.")
      print("  chani: ", self.chani)
      print("  cx cy cz: ", cx, cy, cz)
      print("  stage: ", sx, sy, sz)
      sys.exit(1)
    #
  def parse1(self, mm):
    self.chani = int(mm[0])
    #
    bx=float(mm[2]); by=float(mm[3]); bz=float(mm[4]);
    cx=float(mm[6]); cy=float(mm[7]); cz=float(mm[8]);
    #
    self.pos_bx=bx;  self.pos_by=by;  self.pos_bz=bz;
    self.pos_cx=cx;  self.pos_cy=cy;  self.pos_cz=cz;
    #
    #
  def pro1(self):
    m_start   = self.m_start
    m_end     = self.m_end
    dL_step   = self.dL_step
    bx=self.pos_bx; by=self.pos_by; bz=self.pos_bz;
    cx=self.pos_cx; cy=self.pos_cy; cz=self.pos_cz;
    Dbcx=cx-bx;  Dbcy=cy-by;  Dbcz=cz-bz;
    Len_bc = hypot(Dbcx,Dbcy,Dbcz)
    #
    dux=Dbcx/Len_bc; duy=Dbcy/Len_bc; duz=Dbcz/Len_bc;
    start_x=bx+dux*m_start;
    start_y=by+duy*m_start;
    start_z=bz+duz*m_start;
    step_dx = start_x + dux*dL_step
    step_dy = start_y + duy*dL_step
    step_dz = start_z + duz*dL_step
    #
    self.Len_sweep = Len_bc - m_start - m_end
    #
    self.n_im = int(self.Len_sweep/dL_step)
    self.start_x=start_x;
    self.start_y=start_y;
    self.start_z=start_z;
    self.step_dx = step_dx;
    self.step_dy = step_dy;
    self.step_dz = step_dz;
    #
    self.im_pos_x = []
    self.im_pos_y = []
    self.im_pos_z = []
    for i in range(self.n_im):
      x = start_x + step_dx * i
      y = start_y + step_dy * i
      z = start_z + step_dz * i
      self.im_pos_x.append(x)
      self.im_pos_y.append(y)
      self.im_pos_z.append(z)
    #
    #
  def get_stage_coords_xy(self, ux,uy):
    sx = ux * self.stage_units_per_mm
    sx = self.stage_center_x - sx
    sy = uy * self.stage_units_per_mm
    sy = sy + self.stage_center_y
    return sx, sy
    #
  def get_user_coords_xy(self, sx,sy):
    ux = self.stage_center_x - sx
    ux /= self.stage_units_per_mm
    uy = sy - self.stage_center_y
    uy /= self.stage_units_per_mm
    return ux, uy
    #
    #
  def reset_edges(self):
    #
    # Go to (bx,by,bz).
    x=self.pos_bx; y=self.pos_by; z=self.pos_bz;
    self.stage.go_user_xyz(x,y,z);
    #
    # Ask for adjustment.
    print()
    print( 'Channel '+str(self.chani)+', point b.' )
    print( '  Adjust position and hit enter,')
    print( '  x exits with no change.')
    uin = input('  >> ')
    if uin == 'x' or uin == 'q':  return 1
    bx, by, bz = self.stage.sread_user_xyz()
    if self.run_mode == 'serial':
      self.pos_bx=bx;
      self.pos_by=by;
      self.pos_bz=bz;
    #
    # Go to (cx,cy,cz).
    x=self.pos_cx; y=self.pos_cy; z=self.pos_cz;
    self.stage.go_user_xyz(x,y,z);
    #
    # Ask for adjustment.
    print()
    print( 'Channel '+str(self.chani)+', point c.' )
    print( '  Adjust position and hit enter,')
    print( '  x exits with no change.')
    uin = input('  >> ')
    if uin == 'x' or uin == 'q':  return 1
    cx, cy, cz = self.stage.sread_user_xyz()
    if self.run_mode == 'serial':
      self.pos_cx=cx;
      self.pos_cy=cy;
      self.pos_cz=cz;
    #
    return 0
    #
  def go_run(self, imi):
    #
    for i in range(self.n_im):
      print('.',end='',flush=True)
      posx = self.im_pos_x[i]
      posy = self.im_pos_y[i]
      posz = self.im_pos_z[i]
      #
      # AF:
      # We need to get the actual time
      # the image was taken and save that
      # to a log file.
      #
      # 1.  Prior:   Move the stage.
      self.stage.go_user_xyz(posx,posy,posz)
      #
      # 2.  Basler:  Take the image and save.
      # AF.  Keep track of image index and
      #      pass it to "take_image".
      #      We need to keep track of it at
      #      a high level to save in a log file.
      self.camera.take_image(imi)
      #
      imi += 1
      #
    print()
    return imi
    #
  def gou_1b(self):
    ou = ''
    ou += '\n'
    ou += '# ________________________\n'
    ou += '!channel\n'
    ou += '!order_i ; '+str(self.order_i)+'\n'
    ou += '!chani   ; '+str(self.chani)+'\n'
    ou += '!n_im    ; '+str(self.n_im)+'\n'
    ou += '!ims\n'
    ou += '# imi ; L         ; x         ; y         ; z\n'
    for i in range(self.n_im):
      x = self.im_pos_x[i];
      y = self.im_pos_y[i];
      z = self.im_pos_z[i];
      L = i * self.dL_step;
      ou += '{:5d}'.format( i )
      ou += ' ; {:9.4f}'.format( L )
      ou += ' ; {:9.4f}'.format( x )
      ou += ' ; {:9.4f}'.format( y )
      ou += ' ; {:9.4f}'.format( z )
      ou += '\n'
    return ou
    #
  def gou_1c(self):
    # Save stage coords.
    coords = self.stage.get_stage_coords
    in_lims = self.stage.is_in_limits_xyz
    #
    ou = ''
    ou += '\n'
    ou += '# ________________________\n'
    ou += '!channel\n'
    ou += '!order_i ; '+str(self.order_i)+'\n'
    ou += '!chani   ; '+str(self.chani)+'\n'
    ou += '!n_im    ; '+str(self.n_im)+'\n'
    ou += '!ims\n'
    ou += '# imi ; L         ; x         ; y         ; z         ; in limits\n'
    for i in range(self.n_im):
      ux = self.im_pos_x[i];
      uy = self.im_pos_y[i];
      uz = self.im_pos_z[i];
      x,y,z = coords(ux,uy,uz)
      inlim = '.'
      if not in_lims(x,y,z): inlim = 'x'
      L = i * self.dL_step;
      ou += '{:5d}'.format( i )
      ou += ' ; {:9.4f}'.format( L )
      ou += ' ; {:9.1f}'.format( x )
      ou += ' ; {:9.1f}'.format( y )
      ou += ' ; {:9.1f}'.format( z )
      ou += ' ; '+inlim
      ou += '\n'
    return ou
    #



