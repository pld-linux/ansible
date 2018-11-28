Summary:	SSH-based configuration management, deployment, and task execution system
Name:		ansible
Version:	2.6.8
Release:	0.1
License:	GPL v3+
Group:		Development/Libraries
Source0:	https://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
# Source0-md5:	3e8442a9c50abcb5bed39e4676e3641f
Patch0:		https://github.com/glensc/ansible/compare/pm-poldek.patch
# Patch0-md5:	91dd49cb9c64c52615aec95341c40128
Patch1:		https://github.com/glensc/ansible/compare/rc.d-systemd.patch
# Patch1-md5:	a51f047c5514124dc29221f3336be402
URL:		http://ansible.github.com/
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-PyYAML
Requires:	python-jinja2
Requires:	python-modules
Requires:	python-paramiko
%if "%{py_ver}" < "2.6"
Requires:	python-simplejson
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

%prep
%setup -q
%patch0 -p1

%build
%py_build
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
%py_install

#py_postclean

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_mandir}}
sed -re '/^#/ !s,[^#]+$,#&,' examples/hosts > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hosts
cp -p examples/ansible.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -a docs/man/* $RPM_BUILD_ROOT%{_mandir}

%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/.gitdir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hosts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(755,root,root) %{_bindir}/ansible
%attr(755,root,root) %{_bindir}/ansible-doc
%attr(755,root,root) %{_bindir}/ansible-playbook
%attr(755,root,root) %{_bindir}/ansible-pull
%{_bindir}/ansible-config
%{_bindir}/ansible-connection
%{_bindir}/ansible-console
%{_bindir}/ansible-galaxy
%{_bindir}/ansible-inventory
%{_bindir}/ansible-vault
%{_mandir}/man1/ansible-config.1*
%{_mandir}/man1/ansible-console.1*
%{_mandir}/man1/ansible-galaxy.1*
%{_mandir}/man1/ansible-inventory.1*
%{_mandir}/man1/ansible-vault.1*
%{_mandir}/man1/ansible.1*
%{_mandir}/man1/ansible-doc.1*
%{_mandir}/man1/ansible-playbook.1*
%{_mandir}/man1/ansible-pull.1*
%{py_sitescriptdir}/ansible
%{py_sitescriptdir}/ansible-%{version}-*.egg-info
