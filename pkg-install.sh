#!/bin/bash

cd "$(dirname "$0")"
. ./conf.inc

PKG_VOXIND=build.i386.sig/voxind_$MAJ.$MIN.$REV-${PKG}_i386.rpm
PKG_LIBVOXIN=build.amd64.sig/libvoxin1_$MAJ.$MIN.$REV-${PKG}_amd64.rpm

if [ "$(id -u)" != "0" ]; then
	echo "install.sh must be run as root"
	exit 1
fi

if [ ! -e "$PKG_VOXIND" ]; then
	echo "$PKG_VOXIND not found"
	exit 1
fi
if [ ! -e "$PKG_LIBVOXIN" ]; then
	echo "$PKG_LIBVOXIN not found"
	exit 1
fi

dnf -y remove voxind
dnf -y remove libvoxin1

dnf install -y "$PKG_VOXIND"
dnf install -y "$PKG_LIBVOXIN"

