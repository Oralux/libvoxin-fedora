Name: voxind           
Version:        1.1.7
Release:        1%{?dist}
Summary:        Voxin, text-to-speech based on IBM TTS

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            https://github.com/Oralux/libvoxin
Source0:        %{url}/archive/%{version}.tar.gz
Patch0:         libdir.patch

BuildRequires:  gcc make

%description
Voxin is an easily installable add-on which provides yet another
text-to-speech to blind users of GNU/Linux. It calls the eci API
provided by IBM TTS SDK: https://sourceforge.net/projects/ibmtts-sdk

%prep
%setup -q
%patch0 -p1

%build
RFS=%{buildroot} ./build.sh voxind debug


%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/voxind-%{version}/src
install -d 0755 %{buildroot}/%{_bindir}
install -m 0755 voxind/voxind %{buildroot}/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%license LICENSE
%{_bindir}/voxind

%changelog
* Sun Apr 30 2017 Gilles Casse <gcasse@oralux.org> 1.1.7-1
- Initial package
