%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Memory-mapped key-value database
Name:		lmdb
Version:	0.9.23
Release:	1
License:	OpenLDAP
Group:		System/Libraries
Url:		http://symas.com/mdb/
# Source built from git. To get the tarball, execute following commands:
# $ export VERSION=%%{version}
# $ git clone git://gitorious.org/mdb/mdb.git lmdb && pushd lmdb
# $ git checkout tags/LMDB_$VERSION && popd
# $ tar cvzf lmdb-$VERSION.tar.gz -C lmdb/libraries/ liblmdb
Source0:	https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
# Patch description in the corresponding file
Patch0:		lmdb-make.patch

%description
LMDB is an ultra-fast, ultra-compact key-value embedded data store developed
by for the OpenLDAP Project. By using memory-mapped files, it provides the
read performance of a pure in-memory database while still offering the
persistence of standard disk-based databases, and is only limited to the
size of the virtual address space.

%files
%{_bindir}/mdb_*
%{_mandir}/man1/mdb_*.1*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared library for %{name}.

%files -n %{libname}
%doc libraries/lib%{name}/COPYRIGHT libraries/lib%{name}/CHANGES libraries/lib%{name}/LICENSE
%{_libdir}/liblmdb.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%{_includedir}/lmdb.h
%{_libdir}/liblmdb.so

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-LMDB_%{version}
%patch0 -p1 -b .make

%build
pushd libraries/lib%{name}
%make CC=%{__cc} XCFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%install
pushd libraries/lib%{name}
# make install expects existing directory tree
mkdir -m 0755 -p %{buildroot}%{_bindir}
mkdir -m 0755 -p %{buildroot}%{_includedir}
mkdir -m 0755 -p %{buildroot}%{_libdir}
mkdir -m 0755 -p %{buildroot}%{_mandir}/man1

%makeinstall_std \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	mandir=%{_mandir}

