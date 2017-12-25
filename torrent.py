USB_MOUNT = '/mnt/torrent'

import os
import time
import transmissionrpc
from OmegaExpansion import oledExp

status  = oledExp.driverInit()
oledExp.setTextColumns()

while True:
  statvfs = os.statvfs(USB_MOUNT)
  total = float(statvfs.f_blocks) * statvfs.f_frsize / 1000000000
  free = float(statvfs.f_bfree) * statvfs.f_frsize / 1000000000
  oledExp.setCursor(0, 0)
  oledExp.write('Date: ' + time.strftime("%d %b %y %H:%M"))
  oledExp.setCursor(1, 0)
  oledExp.write('Free: {:.4}/{:.4} GB'.format(free, total))
  time.sleep(5)
