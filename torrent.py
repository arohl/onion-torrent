import os
import time
import transmissionrpc
from OmegaExpansion import oledExp

status  = oledExp.driverInit()
oledExp.setTextColumns()

while True:
  statvfs = os.statvfs('/tmp/mounts/USB-A2')
  total = float(statvfs.f_blocks) * statvfs.f_frsize / 1000000000
  free = float(statvfs.f_bfree) * statvfs.f_frsize / 1000000000
  oledExp.write('Free: {:.3}/{:.3} GB'.format(free, total))
  oledExp.setCursor(0, 0)
  time.sleep(5)