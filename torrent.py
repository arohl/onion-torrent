USB_MOUNT = '/mnt/torrent'
SLEEP = 2

import os
import time
import transmissionrpc
from OmegaExpansion import oledExp

status  = oledExp.driverInit()
oledExp.setTextColumns()

while True:
  # find size of free space on USB
  statvfs = os.statvfs(USB_MOUNT)
  total = float(statvfs.f_blocks) * statvfs.f_frsize / 1000000000
  free = float(statvfs.f_bfree) * statvfs.f_frsize / 1000000000
  # find transmission info
  tc = transmissionrpc.Client('localhost', port=9091)
  torrents=tc.get_torrents()
  download = False
  rateDownload = 0
  rateUpload = 0
  for t in torrents:
    if t.status == 'downloading':
      download = True
      filename = t.name
      percentDone = t.percentDone
    rateUpload += t.rateUpload
    rateDownload += t.rateDownload
  oledExp.setCursor(0, 0)
  oledExp.write('Date: ' + time.strftime("%d %b %y %H:%M"))
  oledExp.setCursor(1, 0)
  oledExp.write('Free: {:.4}/{:.4} GB'.format(free, total))
  oledExp.setCursor(2, 0)
  oledExp.write('Download: {:>5} kbps'.format(rateDownload/1000))
  oledExp.setCursor(3, 0)
  oledExp.write('Upload:   {:>5} kbps'.format(rateUpload/1000))
  oledExp.setCursor(4, 0)
  if download:
    oledExp.write('{:<42}'.format('File: ' + filename))
  else:
    oledExp.write('{:<42}'.format(' '))
  oledExp.setCursor(6, 0)
  if download:
    noStars = int(percentDone*21)
    oledExp.write('{:<21}'.format('*'*noStars))
  else:
    oledExp.write('{:<21}'.format(' '))
  time.sleep(SLEEP)
