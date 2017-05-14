#!/bin/bash -x
cd "$(dirname "$0")"
. ./conf.inc

PV=$MAJ.$MIN.$REV

LIST="wget fedpkg rpmlint"
rpm -ql $LIST &> /dev/null    
if [ "$?" != "0" ]; then
    echo "Install the following packages: $LIST"
    exit 1
fi

function build_pkg() {
    local PN=$1
    local BUILD_DIR=build/$PN-$PV
    rm -rf $BUILD_DIR
    mkdir -p $BUILD_DIR

    cp build/$ARCHIVE fedora.$PN/* $BUILD_DIR

    # cp build/$ARCHIVE $BUILD_DIR/${PN}_$PV.orig.tar.gz
    tar -C $BUILD_DIR -zxf build/$ARCHIVE
    pushd $BUILD_DIR
    mv libvoxin-$PV $PN-$PV
    tar -cf $ARCHIVE $PN-$PV
    rm -rf $PN-$PV
    fedpkg --release f25 local
    find . -name "*rpm" | while read i; do echo "--> $i"; rpmlint $i; done
    popd
}

[ ! -d build ] && mkdir build
cd build
download
cd ..


if [ "$(uname -m)" = "x86_64" ]; then
    export DEB_HOST_ARCH=amd64
    rm -rf build.x86_64
    mkdir -p build.x86_64
    
    build_pkg libvoxin
    mv build/libvoxin-$PV/libvoxin*src.rpm build/libvoxin-$PV/x86_64 build.x86_64
else
    export DEB_HOST_ARCH=i386
    rm -rf build.i686
    mkdir -p build.i686    

    build_pkg voxind
    mv build/voxind-$PV/voxind*src.rpm build/voxind-$PV/i686 build.i686

    build_pkg libvoxin
    mv build/libvoxin-$PV/libvoxin*src.rpm build.i686
    mv build/libvoxin-$PV/i686/* build.i686/i686
fi

