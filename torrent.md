### Fresh Install

Used web interface to do a *Factory Restore*. Called the computer *onion-torrent*

```bash
opkg update
df -h
```

```
Filesystem                Size      Used Available Use% Mounted on
/dev/root                 5.5M      5.5M         0 100% /rom
tmpfs                    61.4M    212.0K     61.2M   0% /tmp
tmpfs                    61.4M     60.0K     61.3M   0% /tmp/root
tmpfs                   512.0K         0    512.0K   0% /dev
/dev/mtdblock6           25.1M      2.6M     22.4M  11% /overlay
overlayfs:/overlay       25.1M      2.6M     22.4M  11% /
```

### Increase disk by adding SDHC and USB storage
Install appropriate packages. Note problem with kernel mismatch for *kmod-fs-ext4* so ignore dependencies

```
opkg install e2fsprogs
opkg install kmod-fs-ext4 —nodeps
```

Set up SDHC to provide extra disk space for system

```
mkfs.ext4 /dev/mmcblk0p1
mkdir /mnt/mmcblk0p1
mount /dev/mmcblk0p1 /mnt/mmcblk0p1/
mount /dev/mmcblk0p1  /mnt/ ; tar -C /overlay -cvf - . | tar -C /mnt/ -xf - ; umount /mnt/
```

Set up USB to provide torrent download directory

```
mkfs.ext4 /dev/sda1
mkdir /mnt/sda1
mount /dev/sda1 /mnt/sda1
```

Set to auto mount on relevant directories
```
mkdir /mnt/torrent
opkg install block-mount
block detect > /etc/config/fstab
vi /etc/config/fstab
```

Look for the line:

```
option  target  '/mnt/<device name>'
```
and change it to:

```
option target '/overlay'
```

Then, look for the line:

```
option  enabled '0'
```

and change it to:

```
option  enabled '1'
```

Repeat for USB disk to mount on */mnt/torrent* and reboot.

### Install common packages for development
```
opkg install vim bash python git
vi /etc/passwd
```

and set default shell to */bin/bash*
