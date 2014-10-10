#!/bin/bash
wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.13.tar.gz
gzip -dc hdf5-1.8.13.tar.gz | tar xf -
cd hdf5-1.8.13
./configure --prefix=/usr/local
make
sudo make install
sudo yum install -y python-devel
sudo yum install -y python-pip
sudo pip install numpy h5py boto
sudo sh -c  "echo '/usr/local/lib' > /etc/ld.so.conf.d/usrlocal.conf"
sudo ldconfig -v