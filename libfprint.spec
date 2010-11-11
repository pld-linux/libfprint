#
# Conditional build:
%bcond_with	static_libs	# don't build static library
#
Summary:	Fingerprint reader library
Summary(pl.UTF-8):	Biblioteka do obsługi czytników linii papilarnych
Name:		libfprint
Version:	0.0.6
Release:	0.7
License:	LGPL v2.1
Group:		Libraries
Source0:	http://dl.sourceforge.net/fprint/%{name}-%{version}.tar.bz2
# Source0-md5:	4f47b46021b186488b60aaa97f90fe43
URL:		http://reactivated.net/fprint/wiki/Libfprint
BuildRequires:	ImageMagick-devel
BuildRequires:	glib2-devel
BuildRequires:	libusb-compat-devel
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open source software library, written in C, designed to make it easy
for application developers to add support for consumer fingerprint
readers to their software.

%description -l pl.UTF-8
Napisana w C, biblioteka o otwartym kodzie, zaprojektowana aby ułatwić
programistom dodawanie obsługi czytników linii papilarnych do ich
oprogramowania.

%package devel
Summary:	libfprint header files
Summary(pl.UTF-8):	Pliki nagłówkowe libfprint
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel

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

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}

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
%doc AUTHORS ChangeLog HACKING README THANKS TODO
%attr(755,root,root) %{_libdir}/libfprint.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfprint.so*
%dir %{_includedir}/libfprint
%{_includedir}/libfprint/fprint.h
%{_pkgconfigdir}/libfprint.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfprint.a
%endif
