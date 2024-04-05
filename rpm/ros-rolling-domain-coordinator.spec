%{?!ros_distro:%global ros_distro rolling}
%global pkg_name domain_coordinator
%global normalized_pkg_name %{lua:return (string.gsub(rpm.expand('%{pkg_name}'), '_', '-'))}

Name:           ros-rolling-domain-coordinator
Version:        0.12.0
Release:        2%{?dist}
Summary:        ROS %{pkg_name} package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  bloom-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel

%{?bloom_package}

%description
A tool to coordinate unique ROS_DOMAIN_IDs across multiple processes


%package devel
Release:        %{release}%{?release_suffix}
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-runtime%{?_isa} = %{version}-%{release}

%description devel
A tool to coordinate unique ROS_DOMAIN_IDs across multiple processes


%package runtime
Release:        %{release}
Summary:        %{summary}

%description runtime
A tool to coordinate unique ROS_DOMAIN_IDs across multiple processes


%prep
%autosetup -p1


%generate_buildrequires
%bloom_buildrequires


%build
%py3_build


%install
%py3_install -- --prefix "%{bloom_prefix}"


%if 0%{?with_tests}
%check
# Look for a directory with a name indicating that it contains tests
TEST_TARGET=$(ls -d * | grep -m1 "^\(test\|tests\)" ||:)
if [ -n "$TEST_TARGET" ] && %__python3 -m pytest --version; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
%__python3 -m pytest $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif


%files devel
%dir %{bloom_prefix}
%ghost %{bloom_prefix}/share/%{pkg_name}/package.xml


%files runtime
%{bloom_prefix}


%changelog
* Wed Mar 20 2024 Brandon Ong <brandon@openrobotics.org> - 0.12.0-2
- Autogenerated by Bloom