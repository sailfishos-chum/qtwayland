%global qt_version 5.15.10

Summary: Qt5 - Wayland platform support and QtCompositor module
Name: opt-qt5-qtwayland
Version: 5.15.10+kde52
Release: 1%{?dist}

License: LGPLv3
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_opt_qt5_archdatadir}/qml/.*\\.so$

%{?opt_qt5_default_filter}

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-static
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel

BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libudev)

Requires: opt-qt5-qtbase-gui >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
%{?opt_qt5_default_filter}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%license LICENSE.*
%{_opt_qt5_libdir}/libQt5WaylandCompositor.so.5*
%{_opt_qt5_libdir}/libQt5WaylandClient.so.5*
%{_opt_qt5_plugindir}/wayland-decoration-client/
%{_opt_qt5_plugindir}/wayland-graphics-integration-server
%{_opt_qt5_plugindir}/wayland-graphics-integration-client
%{_opt_qt5_plugindir}/wayland-shell-integration
%{_opt_qt5_plugindir}/platforms/libqwayland-egl.so
%{_opt_qt5_plugindir}/platforms/libqwayland-generic.so
%{_opt_qt5_qmldir}/QtWayland/

%files devel
%{_opt_qt5_bindir}/qtwaylandscanner
%{_opt_qt5_headerdir}/QtWaylandCompositor/
%{_opt_qt5_headerdir}/QtWaylandClient/
%{_opt_qt5_libdir}/libQt5WaylandCompositor.so
%{_opt_qt5_libdir}/libQt5WaylandClient.so
%{_opt_qt5_libdir}/libQt5WaylandCompositor.prl
%{_opt_qt5_libdir}/libQt5WaylandClient.prl
%{_opt_qt5_libdir}/cmake/Qt5WaylandCompositor/Qt5WaylandCompositorConfig*.cmake
%{_opt_qt5_libdir}/pkgconfig/*.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/*.pri
%{_opt_qt5_libdir}/cmake/Qt5WaylandCompositor/
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*.cmake
%{_opt_qt5_libdir}/cmake/Qt5WaylandClient/
