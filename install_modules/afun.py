#!/usr/bin/python3


def get_true_false_str(v):
  if v == 'true':  return True
  if v == 'True':  return True
  if v == '1':  return True
  if v == 'false':  return False
  if v == 'False':  return False
  if v == '0':  return False
  print("Error.  Bad true_false str.")
  print("  v: ", v)
  sys.exit(1)

def get_str_of_true_false(v):
  if v:  return 'true'
  return        'false'





