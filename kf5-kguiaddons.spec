#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	5.116
%define		qtver		5.15.2
%define		kfname		kguiaddons

Summary:	Utilities for graphical user interfaces
Summary(pl.UTF-8):	Narzędzia do graficznych interfejsów użytkownika
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	10ae58da0ac1b99eb78a8e40c9a39183
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5WaylandClient >= %{qtver}
BuildRequires:	Qt5WaylandClient-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-plasma-wayland-protocols-devel >= 1.7.0
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel >= 1.9
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-proto-kbproto-devel
BuildRequires:	xz
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5WaylandClient >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
Requires:	kf5-dirs
Requires:	wayland >= 1.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
The KDE GUI addons provide utilities for graphical user interfaces in
the areas of colors, fonts, text, images, keyboard input.

%description -l pl.UTF-8
Pakiet dodatków KDE GUI zapewnia narzędzia do graficznych interfejsów
użytkownika w obszarze kolorów, fontów, tekstu, obrazów i wejścia z
klawiatury.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Gui-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5GuiAddons.so.5
%attr(755,root,root) %{_libdir}/libKF5GuiAddons.so.*.*
%{_datadir}/qlogging-categories5/kguiaddons.categories
%attr(755,root,root) %{_bindir}/kde-geo-uri-handler
%{_desktopdir}/google-maps-geo-handler.desktop
%{_desktopdir}/openstreetmap-geo-handler.desktop
%{_desktopdir}/qwant-maps-geo-handler.desktop
%{_desktopdir}/wheelmap-geo-handler.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KGuiAddons
%{_libdir}/cmake/KF5GuiAddons
%{_libdir}/libKF5GuiAddons.so
%{qt5dir}/mkspecs/modules/qt_KGuiAddons.pri
