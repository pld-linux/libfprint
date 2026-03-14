Summary:	Fingerprint reader library
Summary(pl.UTF-8):	Biblioteka do obsługi czytników linii papilarnych
Name:		libfprint
Version:	1.94.10
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/libfprint/libfprint/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	12482afcfd9026d000d06dbe762b528f
Patch0:		vaio-sx.patch
URL:		https://fprint.freedesktop.org/
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk+3-devel
BuildRequires:	gudev-devel
BuildRequires:	libgusb-devel >= 0.2.0
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja
BuildRequires:	openssl-devel >= 3.0
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.727
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.68
Requires:	libgusb >= 0.2.0
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
Requires:	glib2-devel >= 1:2.68
Requires:	libgusb-devel >= 0.2.0

%description devel
libfprint header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe libfprint.

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
BuildArch:	noarch

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
%patch -P0 -p1

%build
%meson \
	-Dgtk-examples=true \
	-Dinstalled-tests=false

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%meson_install

cp -p examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING.md NEWS README.md THANKS
%attr(755,root,root) %{_libdir}/libfprint-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfprint-2.so.2
%{_libdir}/girepository-1.0/FPrint-2.0.typelib
%{_datadir}/metainfo/org.freedesktop.libfprint.metainfo.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfprint-2.so
%{_includedir}/libfprint-2
%{_pkgconfigdir}/libfprint-2.pc
%{_datadir}/gir-1.0/FPrint-2.0.gir
%{_examplesdir}/%{name}-%{version}

%files demo
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gtk-libfprint-test
%{_desktopdir}/org.freedesktop.libfprint.Demo.desktop
%{_iconsdir}/org.freedesktop.libfprint.Demo.png
%{_datadir}/metainfo/org.freedesktop.libfprint.Demo.appdata.xml

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfprint-2

%files -n udev-libfprint
%defattr(644,root,root,755)
/lib/udev/rules.d/70-libfprint-2.rules
