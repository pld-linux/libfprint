#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Fingerprint reader library
Summary(pl.UTF-8):	Biblioteka do obsługi czytników linii papilarnych
Name:		libfprint
Version:	0.5.1
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.xz
# Source0-md5:	f52ac662d89fb82a441dacb0bac36c13
URL:		http://reactivated.net/fprint/wiki/Libfprint
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	libusb-devel >= 0.9.1
BuildRequires:	nss-devel
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
Requires:	gdk-pixbuf2-devel >= 2.0
Requires:	glib2-devel >= 1:2.28
Requires:	libusb-devel >= 0.9.1
Requires:	nss-devel

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

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libfprint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfprint.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfprint.so
%{_libdir}/libfprint.la
%dir %{_includedir}/libfprint
%{_includedir}/libfprint/fprint.h
%{_pkgconfigdir}/libfprint.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfprint.a
%endif

%files -n udev-libfprint
%defattr(644,root,root,755)
/lib/udev/rules.d/60-fprint-autosuspend.rules
