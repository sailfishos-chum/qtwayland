%global qt_version 5.15.8

Summary: Qt5 - Wayland platform support and QtCompositor module
Name: opt-qt5-qtwayland
Version: 5.15.8
Release: 1%{?dist}

License: LGPLv3
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_opt_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{version}
BuildRequires: opt-qt5-qtbase-static
BuildRequires: opt-qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
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

%description
%{summary}.

%package devel
Summary: Development files for %{name}
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


%changelog
* Thu Jan 05 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-1
- 5.15.8

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.7-1
- 5.15.7

* Tue Sep 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-1
- 5.15.6

* Thu Aug 25 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-4
- Re-enable CSD backports from Qt6 (will be used by QGnomePlatform)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-2
- Keep toplevel windows in the top left corner of the screen

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-1
- 5.15.5

* Mon May 16 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.4-1
- 5.15.4

* Fri Apr 15 2022 Kenneth Topp <toppk@bllue.org> - 5.15.3-2
- Pull in latest kde/5.15 branch fixes

* Fri Mar 04 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.3-1
- 5.15.3

* Fri Feb 11 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.2-21
- Pull in latest kde/5.15 branch fixes
  + backport a fix to crashes caused by patch 0043

* Fri Feb 04 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-20
- re-enable nvidia-related patches (44,100)

* Thu Feb 03 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.2-19
- Disable some upstream patches causing a crash on Wayland sessions
  bz#2049560

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.2-18
- Include potential upstream fix for Plasma panel freezes

* Thu Jan 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.2-17
- Pull in latest kde/5.15 branch fixes

* Tue Jan 18 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.2-16
- Pull in latest kde/5.15 branch fixes

* Mon Dec 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-15
- Pull in latest kde/5.15 branch fixes

* Mon Oct 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-14
- Update clipboard patch

* Mon Oct 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-13
- Backport clipboard fixes
  Resolves: bz#1957503

* Tue Sep 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-12
- Pull in latest kde/5.15 branch fixes

* Tue Sep 07 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-11
- Include only some Qt6 API additions for better client-side decoration support

* Tue Sep 07 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-10
- Disable decoration shadow support

* Mon Aug 30 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-9
- Client: include decoration fixes and improvements from Qt6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-7
- Client: expose toplevel window state (change from Qt6)

* Tue Apr 27 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-6
- Pull in latest fixes from https://invent.kde.org/qt/qt/qtwayland

* Tue Apr 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-5
- Backport changes from Qt 5.15.3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 09:32:16 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-3
- Scanner: Avoid accessing dangling pointers in destroy_func()

* Tue Nov 24 07:54:16 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 09:30:47 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jan Grulich <jgrulich@redhat.com> - 5.14.2-4
- Backport upstream patches
  Resolves: bz#1860455

* Thu Apr 30 2020 Ivan Mironov <mironov.ivan@gmail.com> - 5.14.2-3
- Cherry-pick fix for clipboard related crash from v5.15.0

* Tue Apr 21 2020 Jan Grulich <jgrulich@redhat.com> - 5.14.2-2
- Fix bold font rendering
  Resolves: bz#1823984

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-2
- Add support for primary-selection-unstable-v1 protocol
- Fix inverse repeat rate implementation

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Fri Oct 18 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-2
- Client: Fix 100ms freeze when applications do not swap after deliverUpdateRequest

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Tue Jul 30 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-6
- Do not redraw decorations everytime

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-5
- Use Gnome platform theme on Gnome Wayland sessions
  Resolves: bz#1732129

* Thu Jul 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-4
- Pull in upstream fixes
- Disable patch which is not needed anymore because of qtbase change

* Tue Jul 02 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-3
- Pull in upstream fixes

* Thu Jun 27 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-2
- Pull in upstream fixes

* Fri Jun 14 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Fri May 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-4
- rebuild again (#1711115)

* Fri May 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-3
- rebuild (qt5-qtbase)

* Thu May 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-2
- drop BR: pkgconfig(glesv2)

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0
- use %%make_build %%ldconfig_scriptlets

* Tue Mar 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-2
- Do not crash when opening dialogs

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-1
- 5.10.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.0-2
- Do not recreate hidden egl surfaces
  QTBUG-65553

* Tue Dec 19 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Thu Nov 23 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Mon Oct 09 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- 5.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- .spec cosmetics, Source URL, refer to qt5- builddeps directly

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Tue May 09 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Mon Jan 30 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- New upstream version

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-3
- filter qml provides, BR: qtbase-private-devel qtdeclarative explicitly

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- drop BR: cmake (handled by qt5-rpm-macros now)
- 5.7.1 dec5 snapshot

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Compiled with gcc

* Wed Jun 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Thu Jun 09 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-11
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-10
- rebuild

* Tue Mar 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.6.0-9
- Bump release to 9 so it's higher than the final RC

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-8.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-7
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-6.rc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-5.rc
- use %%opt_qmake_qt5 consistently

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-4.rc
- BR: cmake, update source URL, use %%license

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-3
- Update to final rc release

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-2
- Official rc release

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 rc

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- tighten qtbase dep (#1233829)

* Sun Jul 05 2015 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.5.0-2
- Add xkbcommon to the devel package.

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt5 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.rc
- use %%opt_qmake_qt5 macro

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.rc
- 5.4.0-rc

* Wed Sep 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.4.0-0.alpha1
- Switch from a Git snapshot to a pre-release tarball

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-0.3.20140723git02c499c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.3.0-0.2.20140723git02c499c
- Update

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-0.2.20140529git98dca3b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.3.0-0.1.20140529git98dca3b
- Update and rebuild for Qt 5.3

* Fri Feb 14 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.6.20140202git6d038fb
- A more recent snapshot
- Disable xcomposite compositor until it builds

* Sat Jan 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.6.20131203git6b20dfe
- Enable QtQuick compositor

* Sat Jan 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131203git6b20dfe
- A newer snapshot

* Mon Nov 25 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131125git4f5985c
- Rebase to a later snapshot, drop our patches
- Add license texts

* Sat Nov 23 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.5.20131120git8cd1a77
- Rebuild with EGL backend

* Fri Nov 22 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.4.20131120git8cd1a77
- Rebase to a later snapshot, drop 5.2 ABI patch
- Enable nogl backend

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.0-0.4.20130826git3b0b90b
- rebuild (arm/qreal)

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.3.20130826git3b0b90b
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sun Oct 06 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.2.20130826git3b0b90b
- Bump platform plugin ABI to 5.2 for Qt 5.2 aplha

* Wed Sep 11 2013 Lubomir Rintel <lkundrak@v3.sk> - 5.1.0-0.1.20130826git3b0b90b
- Initial packaging
- Adjustments from review (Rex Dieter, #1008529)




