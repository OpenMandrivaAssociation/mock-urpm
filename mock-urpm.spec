%define modname mock_urpm
%define mockgid  135

Summary:	Builds packages inside chroots
Name:		mock-urpm
Version:	1.3.10
Release:	8
License:	GPLv2+
Group:		Development/Other
Source0:	https://abf.io/soft/%{name}/archive/%{name}-%{version}.tar.gz
URL:		http://wiki.rosalab.ru/en/index.php/Mock-urpm
Patch0:		site-defaults.patch
Patch1:		mock-urpm.loop-control.patch
Patch2:		mock-urpm-umount-proc-when-cleaning-tmp.patch
Patch3:		mock-urpm-1.3.10-do-not-use-urpmi-from-inside-chroot.patch
#BuildRequires:	pkgconfig(python2)
BuildRequires:	shadow
BuildArch:	noarch
Requires:	bsdtar
Requires:	pigz
Requires:	python-ctypes
Requires:	python2-pexpect
Requires:	python-decoratortools
Requires:	usermode-consoleonly
Requires:	python2
Requires:	python-rpm
Suggests:	rpm-build
Requires(pre):	coreutils
Requires(pre):	shadow

%description
Mock-urpm takes an SRPM and builds it in a chroot.

%prep
%setup -q
%autopatch -p1

# Until we get python3 support...
sed -i -e 's,/usr/bin/python,%{__python2},g' py/sbin/*.py

%install
%makeinstall_std PYTHON=%{__python2}
mkdir -p %{buildroot}/%{_bindir}
ln -s %{_bindir}/consolehelper %{buildroot}/%{_bindir}/%{name}
ln -s %{_datadir}/bash-completion/%{name} %{buildroot}/%{_sysconfdir}/bash_completion.d/%{name}

%pre
if [ $1 -eq 1 ]; then #first install
    groupadd -r -f %{name} -g %mockgid >/dev/null 2>&1 || :
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
%dir %{python2_sitelib}/%{modname}
%{python2_sitelib}/%{modname}/*.py
%{python2_sitelib}/%{modname}/*.pyc

#bash_completion files
%{_datadir}/bash-completion/%{name} 
%{_sysconfdir}/bash_completion.d/%{name}

# config files
%config %{_sysconfdir}/%{name}/logging.ini
%config %{_sysconfdir}/%{name}/*.cfg

#plugins
%dir %{python2_sitelib}/%{modname}/plugins
%{python2_sitelib}/%{modname}/plugins/*.py
%{python2_sitelib}/%{modname}/plugins/*.pyc

# docs
%{_mandir}/man1/%{name}.1*

# build dir
%attr(02775, root, %{name}) %dir /var/lib/%{name}

# cache dir
%attr(02775, root, %{name}) %dir /var/cache/%{name}
