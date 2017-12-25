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
opkg install vim bash python python-pip pyOledExp git git-http ca-bundle
vi /etc/passwd
```

and set default shell to */bin/bash*

### Install and configure transmission
```
opkg install transmission-daemon-openssl transmission-web
mkdir -p /mnt/torrent/downloads/incomplete
uci set transmission.@transmission[0].enabled=‘1'
uci set transmission.@transmission[0].config_dir='/etc/transmission’
uci set transmission.@transmission[0].download_dir='/mnt/torrent/downloads’
uci set transmission.@transmission[0].incomplete_dir='/mnt/torrent/downloads/incomplete’
uci set transmission.@transmission[0].incomplete_dir_enabled=‘true'
uci set transmission.@transmission[0].rpc_whitelist_enabled=‘false'
uci commit transmission
/etc/init.d/transmission enable
/etc/init.d/transmission start
```

### Install transmissionrpc
unfortunately the pip installation fails so install from source
```
pip install six
wget https://pypi.python.org/packages/f5/f8/96a979b669a7219cb4299ea5512e1678ba7f59d91bd8a952c51405131768/transmissionrpc-0.11.tar.gz#md5=b2f918593e509f0e66e2e643291b436d
tar -zxvf transmissionrpc-0.11.tar.gz
cd transmissionrpc-0.11
python setup.py install
cd ..
rm -rf transmissionrpc-0.11*
```

### Install script for monitoring transmission
```
mkdir src
cd src
git clone https://github.com/arohl/onion-torrent.git
