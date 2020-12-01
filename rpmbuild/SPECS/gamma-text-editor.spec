Name:           gamma-text-editor
Version:        0.0.3
Release:        0
Summary:        Gamma is a lightweight text editor. It is meant to be an alternative to Gedit or Notepad++.
License:        GPL-3
URL:            https://gitlab.com/hamadmarri/gamma-text-editor

Requires: libgtk-3-0 python3-gobject python3-gobject-Gdk python3-gobject-cairo typelib-1_0-Gtk-3_0 libgtksourceview-4-0 typelib-1_0-GtkSource-4 typelib-1_0-WebKit2-4_0 yelp libvte-2_91-0 vte-devel typelib-1_0-Vte-2.91 ctags

%description
Gamma (Γ) is a lightweight text editor. It is meant to be an alternative to Gedit or Notepad++.
Although the current implementation is tested on linux under Gnome desktop environment,
Gamma can run on Linux, Windows, and Mac if dependencies are installed
(see Dependencies section below).
Gamma uses GTK3 (cross-platform GUI toolkit) and
PyGObject which is
a Python package that provides bindings for GObject based libraries such as GTK, GStreamer,
WebKitGTK, GLib, GIO and many more.
Lightweight, not CPU/RAM hungry
No learning curve (easy/familiar shortcuts, easy use of plugin/extensions)
Fully customizable from A to Z (even the UI layout)
New UX approach for text editors
Easy plugin system
Made using Python for python contributors


%install
mkdir -p "$RPM_BUILD_ROOT"
cp -r ~/rpmbuild/SOURCES/usr/ "$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/
