#!/bin/bash 
SWAPSIZE=2048
SWAPFILE=/mnt/swapfile

echo "Creating $SWAPSIZE MB swap file"
dd if=/dev/zero of=$SWAPFILE bs=1M count=$SWAPSIZE
 
echo "Creating swap"
/sbin/mkswap $SWAPFILE
 
echo "Enabling swap"
sudo /sbin/swapon $SWAPFILE