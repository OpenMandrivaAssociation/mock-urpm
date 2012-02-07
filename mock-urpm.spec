# next four lines substituted by autoconf
%define version 1.1.12
%define release 2
%define name mock-urpm
%define modname mock_urpm
%define target_release Mandriva-2011

Summary: Builds packages inside chroots
Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2+
Group: System/Configuration/Packaging
Source: %{name}-%{version}.tar.gz
URL: http://wiki.mandriva.com/en/Mock-urpm

BuildArch: noarch
Requires: tar
Requires: pigz
Requires: python-ctypes
Requires: python-decoratortools
Requires(pre): shadow-utils
Requires(post): coreutils
BuildRequires: python-devel

%description
Mock takes an SRPM and builds it in a chroot

%prep
%setup -q -n %{name}

%install
make install DESTDIR=$RPM_BUILD_ROOT

#%clean
#rm -rf $RPM_BUILD_ROOT

%pre
if [ $1 -eq 1 ]; then
    groupadd -r -f %{name} >/dev/null 2>&1 || :
    if [ ! -z `env|grep SUDO_USER` ]; then
	usermod -a -G %{name} `env|grep SUDO_USER | cut -f2 -d=` >/dev/null 2>&1 || :
    fi
fi

%post
ln -s %{_datadir}/bash-completion/%{name} %{_sysconfdir}/bash_completion.d/%{name}

arch=$(uname -i)
#make no difference between x86 32bit architectures
if [[ $arch =~ i.86 ]]; then 
    arch=i586
fi
cfg=%{target_release}-$arch.cfg
if [ -e %{_sysconfdir}/%{name}/$cfg ] ; then
    ln -s $cfg %{_sysconfdir}/%{name}/default.cfg
#else
#    echo "Failed resolving a correct default configuration file" 
#    echo "Please, create a symlink for the correct one to %{_sysconfdir}/%{name}/default.cfg"
fi

%postun
rm -f %{_sysconfdir}/bash_completion.d/%{name}
rm -f $cfg %{_sysconfdir}/%{name}/default.cfg
groupdel %{name} >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)

# executables
%{_sbindir}/%{name}

# python stuff
%dir %{python_sitelib}/%{modname}
%{python_sitelib}/%{modname}/*.py
%{python_sitelib}/%{modname}/*.pyc

#bash_completion files
#%{_sysconfdir}/bash_completion.d/%{name}
%{_datadir}/bash-completion/%{name} 

# config files
%config(noreplace) %{_sysconfdir}/%{name}/logging.ini
%config(noreplace) %{_sysconfdir}/%{name}/*.cfg

#plugins
%dir %{python_sitelib}/%{modname}/plugins
%{python_sitelib}/%{modname}/plugins/*.py
%{python_sitelib}/%{modname}/plugins/*.pyc

# docs
%{_mandir}/man1/%{name}.1*

# build dir
%attr(02775, root, %{name}) %dir /var/lib/%{name}

# cache dir
%attr(02775, root, %{name}) %dir /var/cache/%{name}
