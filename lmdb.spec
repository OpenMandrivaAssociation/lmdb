%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Memory-mapped key-value database
Name:		lmdb
Version:	0.9.31
Release:	1
License:	OpenLDAP
Group:		System/Libraries
Url:		https://symas.com/lmdb/
Source0:	https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/lmdb/raw/rawhide/f/lmdb.pc.in
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
%doc %{_mandir}/man1/mdb_*.1*

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
Requires:	%{name} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%{_includedir}/lmdb.h
%{_libdir}/liblmdb.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%prep
%autosetup -n %{name}-LMDB_%{version} -p1

%build
%set_build_flags
cd libraries/lib%{name}
%make_build CC=%{__cc} XCFLAGS="%{optflags} -O3" LDFLAGS="%{build_ldflags}"

%install
cd libraries/lib%{name}
# make install expects existing directory tree
mkdir -m 0755 -p %{buildroot}%{_bindir}
mkdir -m 0755 -p %{buildroot}%{_includedir}
mkdir -m 0755 -p %{buildroot}%{_libdir}
mkdir -m 0755 -p %{buildroot}%{_mandir}/man1

%make_install \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	mandir=%{_mandir}

# Install pkgconfig file
sed -e 's:@PREFIX@:%{_prefix}:g' \
	-e 's:@EXEC_PREFIX@:%{_exec_prefix}:g' \
	-e 's:@LIBDIR@:%{_libdir}:g' \
	-e 's:@INCLUDEDIR@:%{_includedir}:g' \
	-e 's:@PACKAGE_VERSION@:%{version}:g' \
	%{SOURCE1} >lmdb.pc

install -Dpm 0644 -t %{buildroot}%{_libdir}/pkgconfig lmdb.pc
