Summary:	GStreamer Streaming-media framework runtime
Summary(pl.UTF-8):	GStreamer - biblioteki środowiska do obróbki strumieni
Name:		gstreamer0.10
Version:	0.10.36
Release:	7
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
# Source0-md5:	15389c73e091b1dda915279c388b9cb2
Patch0:		gstreamer-without_ps_pdf.patch
Patch1:		gstreamer-eps.patch
Patch2:		gstreamer-inspect-rpm-format.patch
Patch3:		bison3.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison >= 1.875
BuildRequires:	docbook-dtd30-sgml
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils >= 0.6.10
BuildRequires:	flex >= 2.5.31
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.24
BuildRequires:	glibc-misc
BuildRequires:	gnome-doc-tools
BuildRequires:	gobject-introspection-devel >= 0.6.8
BuildRequires:	gtk-doc >= 1.6
BuildRequires:	libtool >= 1.4
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	nasm
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 2.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	transfig
BuildRequires:	xmlto
BuildRequires:	xz
Requires:	glib2 >= 1:2.24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		__gst_inspect	%{_bindir}/gst-inspect-0.10

%define		vmajor		%(echo %{version} | cut -d. -f1,2)
%define		_gstlibdir	%{_libdir}/gstreamer-%{vmajor}
%define		_gstincludedir	%{_includedir}/gstreamer-%{vmajor}

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

%description -l pl.UTF-8
GStreamer to środowisko obróbki danych strumieniowych, bazujące na
grafie filtrów operujących na danych medialnych. Aplikacje używające
tej biblioteki mogą robić wszystko od przetwarzania dźwięku w czasie
rzeczywistym, do odtwarzania filmów i czegokolwiek innego związanego z
mediami. Architektura bazująca na wtyczkach pozwala na łatwe dodawanie
nowych typów danych lub możliwości obróbki.

%package devel
Summary:	Include files for GStreamer streaming-media framework
Summary(pl.UTF-8):	Pliki nagłówkowe do środowiska obróbki strumieni GStreamer
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.24
Requires:	libxml2-devel >= 1:2.6.26
Obsoletes:	gstreamer-plugins-bad-devel < 0.10.10

%description devel
This package contains the includes files necessary to develop
applications and plugins for GStreamer.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do rozwijania aplikacji
i wtyczek do GStreamera.

%package static
Summary:	GStreamer static libraries
Summary(pl.UTF-8):	Biblioteki statyczne GStreamer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of GStreamer libraries.

%description static -l pl.UTF-8
Statyczne wersje bibliotek GStreamer.

%package apidocs
Summary:	GStreamer API documentation
Summary(pl.UTF-8):	Dokumentacja API Gstreamera
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
GStreamer API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Gstreamera.

%prep
%setup -q -n gstreamer-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# po/Makefile.in.in is modified
#{__gettextize}
%{__libtoolize}
%{__aclocal} -I common/m4 -I m4 -I .
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-examples \
	--disable-pspdf \
	--disable-silent-rules \
	--disable-tests \
	--enable-docbook \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_docdir}/gstreamer-devel-%{version},%{rpmlibdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/gstreamer-{%{vmajor},%{version}}
mv $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{version}/{faq,manual,pwg} \
	$RPM_BUILD_ROOT%{_docdir}/gstreamer-devel-%{version}

%find_lang gstreamer --all-name --with-gnome

# no *.la for modules - shut up check files
%{__rm} $RPM_BUILD_ROOT%{_gstlibdir}/lib*.la
# *.la for libs kept - no .private dependencies in *.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f gstreamer.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
# generic launchers
%attr(755,root,root) %{_bindir}/gst-feedback
%attr(755,root,root) %{_bindir}/gst-inspect
%attr(755,root,root) %{_bindir}/gst-launch
%attr(755,root,root) %{_bindir}/gst-typefind
%attr(755,root,root) %{_bindir}/gst-xmlinspect
%attr(755,root,root) %{_bindir}/gst-xmllaunch
# versioned
%attr(755,root,root) %{_bindir}/gst-feedback-0.10
%attr(755,root,root) %{_bindir}/gst-inspect-0.10
%attr(755,root,root) %{_bindir}/gst-launch-0.10
%attr(755,root,root) %{_bindir}/gst-typefind-0.10
%attr(755,root,root) %{_bindir}/gst-xmlinspect-0.10
%attr(755,root,root) %{_bindir}/gst-xmllaunch-0.10
%attr(755,root,root) %{_libdir}/libgstbase-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstbase-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstcheck-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcheck-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstcontroller-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstcontroller-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstdataprotocol-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstdataprotocol-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstnet-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstnet-0.10.so.0
%attr(755,root,root) %{_libdir}/libgstreamer-0.10.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstreamer-0.10.so.0
%dir %{_gstlibdir}
%attr(755,root,root) %{_gstlibdir}/gst-plugin-scanner
%attr(755,root,root) %{_gstlibdir}/libgstcoreelements.so
%attr(755,root,root) %{_gstlibdir}/libgstcoreindexers.so
%{_mandir}/man1/gst-feedback-0.10.1*
%{_mandir}/man1/gst-inspect-0.10.1*
%{_mandir}/man1/gst-launch-0.10.1*
%{_mandir}/man1/gst-typefind-0.10.1*
%{_mandir}/man1/gst-xmlinspect-0.10.1*
%{_mandir}/man1/gst-xmllaunch-0.10.1*
%{_libdir}/girepository-1.0/Gst-0.10.typelib
%{_libdir}/girepository-1.0/GstBase-0.10.typelib
%{_libdir}/girepository-1.0/GstCheck-0.10.typelib
%{_libdir}/girepository-1.0/GstController-0.10.typelib
%{_libdir}/girepository-1.0/GstNet-0.10.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgstbase-0.10.so
%attr(755,root,root) %{_libdir}/libgstcheck-0.10.so
%attr(755,root,root) %{_libdir}/libgstcontroller-0.10.so
%attr(755,root,root) %{_libdir}/libgstdataprotocol-0.10.so
%attr(755,root,root) %{_libdir}/libgstnet-0.10.so
%attr(755,root,root) %{_libdir}/libgstreamer-0.10.so
%{_libdir}/libgstbase-0.10.la
%{_libdir}/libgstcheck-0.10.la
%{_libdir}/libgstcontroller-0.10.la
%{_libdir}/libgstdataprotocol-0.10.la
%{_libdir}/libgstnet-0.10.la
%{_libdir}/libgstreamer-0.10.la
%{_docdir}/gstreamer-devel-%{version}
%{_gstincludedir}
%{_pkgconfigdir}/gstreamer-0.10.pc
%{_pkgconfigdir}/gstreamer-base-0.10.pc
%{_pkgconfigdir}/gstreamer-check-0.10.pc
%{_pkgconfigdir}/gstreamer-controller-0.10.pc
%{_pkgconfigdir}/gstreamer-dataprotocol-0.10.pc
%{_pkgconfigdir}/gstreamer-net-0.10.pc
%{_aclocaldir}/gst-element-check-0.10.m4
%{_datadir}/gir-1.0/Gst-0.10.gir
%{_datadir}/gir-1.0/GstBase-0.10.gir
%{_datadir}/gir-1.0/GstCheck-0.10.gir
%{_datadir}/gir-1.0/GstController-0.10.gir
%{_datadir}/gir-1.0/GstNet-0.10.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgstbase-0.10.a
%{_libdir}/libgstcheck-0.10.a
%{_libdir}/libgstcontroller-0.10.a
%{_libdir}/libgstdataprotocol-0.10.a
%{_libdir}/libgstnet-0.10.a
%{_libdir}/libgstreamer-0.10.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gstreamer-0.10
%{_gtkdocdir}/gstreamer-libs-0.10
%{_gtkdocdir}/gstreamer-plugins-0.10
