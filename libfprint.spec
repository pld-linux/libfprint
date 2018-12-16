#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Fingerprint reader library
Summary(pl.UTF-8):	Biblioteka do obsługi czytników linii papilarnych
Name:		libfprint
Version:	0.8.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/libfprint/libfprint/tags
Source0:	https://gitlab.freedesktop.org/libfprint/libfprint/uploads/4272fab4f37516db5b20d07bb576a4b1/%{name}-%{version}.tar.xz
# Source0-md5:	7cc2ffd39b6f86d127c0581597f855e8
Patch0:		%{name}-gtkdoc.patch
URL:		https://fprint.freedesktop.org/
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	gtk-doc
BuildRequires:	libusb-devel >= 0.9.1
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja
BuildRequires:	nss-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.28
Requires:	libusb >= 0.9.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open source software library, written in C, designed to make it easy
for application developers to add support for consumer fingerprint
readers to their software.

%description -l pl.UTF-8
Napisana w C biblioteka o otwartym kodzie, zaprojektowana aby ułatwić
programistom dodawanie obsługi czytników linii papilarnych do ich
oprogramowania.

%package devel
Summary:	libfprint header files
Summary(pl.UTF-8):	Pliki nagłówkowe libfprint
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28
Requires:	libusb-devel >= 0.9.1
Requires:	nss-devel
Requires:	pixman-devel

%description devel
libfprint header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe libfprint.

%package static
Summary:	Static fprint library
Summary(pl.UTF-8):	Statyczna biblioteka fprint
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static fprint library.

%description static -l pl.UTF-8
Statyczna biblioteka fprint.

%package apidocs
Summary:	API documentation for libfprint library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libfprint
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libfprint library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libfprint.

%package -n udev-libfprint
Summary:	Udev rules for libfprint
Summary(pl.UTF-8):	Reguły udeva dla libfprint
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	udev-core

%description -n udev-libfprint
Udev rules for libfprint.

%description -n udev-libfprint -l pl.UTF-8
Reguły udeva dla libfprint.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Dx11-examples=false \
	%{!?with_static_libs:--default=library=shared}

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%meson_install -C build

install examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING.md NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libfprint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfprint.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfprint.so
%dir %{_includedir}/libfprint
%{_includedir}/libfprint/fprint.h
%{_pkgconfigdir}/libfprint.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfprint.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfprint

%files -n udev-libfprint
%defattr(644,root,root,755)
/lib/udev/rules.d/60-fprint-autosuspend.rules
