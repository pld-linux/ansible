Summary:	Minimal SSH command and control
Name:		ansible
Version:	1.2
Release:	0.11
License:	GPL v3+
Group:		Development/Libraries
Source0:	https://github.com/ansible/ansible/archive/devel.tar.gz?/%{version}-dev.tgz
# Source0-md5:	7dcb52644cbe4e9dc998246e69ca3edc
Patch0:		https://github.com/glensc/ansible/compare/pm-poldek.patch
# Patch0-md5:	91dd49cb9c64c52615aec95341c40128
Patch1:		https://github.com/glensc/ansible/compare/rc.d-systemd.patch
# Patch1-md5:	a51f047c5514124dc29221f3336be402
URL:		http://ansible.github.com/
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
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
%setup -qc
mv %{name}-devel/* .
%patch0 -p1

%build
%{__python} setup.py build
%{__make} modulepages

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

#py_postclean

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir}/%{name},%{_mandir}}
sed -re '/^#/ !s,[^#]+$,#&,' examples/hosts > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hosts
cp -p examples/ansible.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -a docs/man/* $RPM_BUILD_ROOT%{_mandir}
cp -a library/* $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/*.asciidoc.in
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/.gitdir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc VERSION *.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hosts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(755,root,root) %{_bindir}/ansible
%attr(755,root,root) %{_bindir}/ansible-doc
%attr(755,root,root) %{_bindir}/ansible-playbook
%attr(755,root,root) %{_bindir}/ansible-pull
%{_mandir}/man1/ansible.1*
%{_mandir}/man1/ansible-doc.1*
%{_mandir}/man1/ansible-playbook.1*
%{_mandir}/man1/ansible-pull.1*
%{_mandir}/man3/ansible.*.3*
%{_datadir}/%{name}
%{py_sitescriptdir}/ansible
%{py_sitescriptdir}/ansible-%{version}-*.egg-info
