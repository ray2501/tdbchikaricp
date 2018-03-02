#
# spec file for package tdbchikaricp
#

Name:           tdbchikaricp
BuildRequires:  tcl
Version:        0.1
Release:        0
Summary:        Tcl DataBase Connectivity Driver for HikariCP library
Url:            https://github.com/ray2501/tdbchikaricp
License:        MIT
Group:          Development/Libraries/Tcl
BuildArch:      noarch
Requires:       tcl >= 8.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}.tar.gz

%description
Tcl DataBase Connectivity Driver for HikariCP library

This extension needs Tcl >= 8.6, TDBC and tclBlend (or tclJBlend) package.

%prep
%setup -q -n %{name}

%build

%install
dir=%buildroot%{tcl_noarchdir}/%{name}%{version}/tdbc
tclsh ./installer.tcl -path $dir

cat > %{buildroot}%{tcl_noarchdir}/%{name}%{version}/pkgIndex.tcl << 'EOD'
#
# Tcl package index file
#
package ifneeded tdbc::hikaricp 0.1 \
    [list source [file join tdbc hikaricp-0.1.tm]]
EOD

%files
%defattr(-,root,root)
%doc README.md
%{tcl_noarchdir}/%{name}%{version}

%changelog
