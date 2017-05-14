%global maj 1
Name: libvoxin           
Version:        1.1.7
Release:        1%{?dist}
Summary:        Voxin, text-to-speech based on IBM TTS

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            https://github.com/Oralux/libvoxin
Source0:        %{url}/archive/%{version}.tar.gz
Patch0:         libdir.patch

BuildRequires:  gcc gcc-c++ make

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
Voxin is an easily installable add-on which provides yet another
text-to-speech to blind users of GNU/Linux. It calls the eci API
provided by IBM TTS SDK: https://sourceforge.net/projects/ibmtts-sdk

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains the development headers for the library found in
libvoxin. Non-developers likely have little use for this package.


%prep
%setup -q
%patch0 -p1

%build
RFS=%{buildroot} ./build.sh libvoxin debug

%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/libvoxin-%{version}/src
install -d 0755 %{buildroot}/%{_libdir} %{buildroot}/%{_includedir}
install -m 0755 libvoxin/libvoxin.so.* %{buildroot}/%{_libdir}
ln -s %{_libdir}/libvoxin.so.%{version} %{buildroot}/%{_libdir}/libvoxin.so.%{maj}
ln -s %{_libdir}/libvoxin.so.%{maj} %{buildroot}/%{_libdir}/libvoxin.so
install -m 0644 api/eci.h %{buildroot}/%{_includedir}

touch %{buildroot}%{_libdir}/libibmeci.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_sbindir}/update-alternatives --install %{_libdir}/libibmeci.so \
 libibmeci.so %{_libdir}/libvoxin.so.%{version} 10

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove libibmeci.so \
     %{_libdir}/libvoxin.so.%{version}
fi

%files
%license LICENSE
%ghost %{_libdir}/libibmeci.so
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Sun Apr 30 2017 Gilles Casse <gcasse@oralux.org> 1.1.7-1
- Initial package
