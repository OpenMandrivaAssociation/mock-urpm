%define modname mock_urpm

Summary:	Builds packages inside chroots
Name:		mock-urpm
Version:	1.3.10
Release:	0.1
License:	GPLv2+
Group:		Development/Other
Source0:	https://abf.io/soft/%{name}/archive/%{name}-%{version}.tar.gz
URL:		http://wiki.rosalab.ru/en/index.php/Mock-urpm
Patch0:		site-defaults.patch
Patch1:		mock-urpm.loop-control.patch
Patch2:		mock-urpm-umount-proc-when-cleaning-tmp.patch

BuildRequires:	pkgconfig(python)
BuildRequires:	shadow-utils
BuildArch:	noarch
Requires:	tar
Requires:	pigz
Requires:	python-ctypes
Requires:	python-pexpect
Requires:	python-decoratortools
Requires:	usermode-consoleonly
Requires:	python
Requires:	python-rpm
Requires:	rpm-build
Requires(pre):	coreutils
Requires(pre):	shadow-utils

%description
Mock-urpm takes an SRPM and builds it in a chroot.

%prep
%setup -q
%apply_patches

%install
%makeinstall_std
mkdir -p %{buildroot}/%{_bindir}
ln -s %{_bindir}/consolehelper %{buildroot}/%{_bindir}/%{name}
ln -s %{_datadir}/bash-completion/%{name} %{buildroot}/%{_sysconfdir}/bash_completion.d/%{name}

%pre
if [ $1 -eq 1 ]; then #first install
    groupadd -r -f %{name} >/dev/null 2>&1 || :
    if [ ! -z `env|grep SUDO_USER` ]; then
	usermod -a -G %{name} `env|grep SUDO_USER | cut -f2 -d=` >/dev/null 2>&1 || :
    fi
fi

%postun
if [ $1 -eq 0 ]; then # complete removing
  rm -f %{_sysconfdir}/%{name}/default.cfg
  groupdel %{name} >/dev/null 2>&1 || :
fi

%files
%{_sbindir}/%{name}
%{_bindir}/%{name}

#consolehelper and PAM
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/security/console.apps/%{name}

# python stuff
%dir %{python_sitelib}/%{modname}
%{python_sitelib}/%{modname}/*.py
%{python_sitelib}/%{modname}/*.pyc

#bash_completion files
%{_datadir}/bash-completion/%{name} 
%{_sysconfdir}/bash_completion.d/%{name}

# config files
%config %{_sysconfdir}/%{name}/logging.ini
%config %{_sysconfdir}/%{name}/*.cfg

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
