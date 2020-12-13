#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Fingerprint reader library
Summary(pl.UTF-8):	Biblioteka do obsługi czytników linii papilarnych
Name:		libfprint
Version:	1.90.6
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/libfprint/libfprint/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	923d1f1c5aef5ac642b89ef2d95cd055
Patch0:		vaio-sx.patch
Patch1:		0001-nbis-Disable-array-parameter-and-array-bounds-warnin.patch
URL:		https://fprint.freedesktop.org/
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	gtk-doc
BuildRequires:	gtk+3-devel
BuildRequires:	libusb-devel >= 0.9.1
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja
BuildRequires:	nss-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.727
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

%package demo
Summary:	Example libfprint GTK+ image capture program
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description demo
Example libfprint GTK+ image capture program.

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
%setup -q -n %{name}-v%{version}
%patch0 -p1
%patch1 -p1

%build
%meson build \
	-Dgtk-examples=true \
	%{!?with_static_libs:--default=library=shared}

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%meson_install -C build

cp -p examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING.md NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libfprint-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfprint-2.so.2
%{_libdir}/girepository-1.0/FPrint-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfprint-2.so
%{_includedir}/libfprint-2
%{_pkgconfigdir}/libfprint-2.pc
%{_datadir}/gir-1.0/FPrint-2.0.gir
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfprint-2.a
%endif

%files demo
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gtk-libfprint-test
%{_desktopdir}/org.freedesktop.libfprint.Demo.desktop
%{_iconsdir}/org.freedesktop.libfprint.Demo.png
%{_datadir}/metainfo/org.freedesktop.libfprint.Demo.appdata.xml

%defattr(644,root,root,755)
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfprint-2

%files -n udev-libfprint
%defattr(644,root,root,755)
/lib/udev/rules.d/60-libfprint-2-autosuspend.rules
