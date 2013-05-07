Summary:	Minimal SSH command and control
Name:		ansible
Version:	1.1
Release:	0.2
License:	GPL v3+
Group:		Development/Libraries
Source0:	https://github.com/ansible/ansible/archive/release%{version}.tar.gz
# Source0-md5:	92e66d233fd7130ea23dfb61ba3b4856
URL:		http://ansible.github.com/
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-PyYAML
Requires:	python-jinja2
Requires:	python-paramiko
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

%prep
%setup -q -n %{name}-release%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir}/%{name},%{_mandir}/man1}
sed -re '/^#/ !s,[^#]+$,#&,' examples/hosts > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hosts
cp -p docs/man/man1/ansible.1 $RPM_BUILD_ROOT%{_mandir}/man1/ansible.1
cp -p docs/man/man1/ansible-playbook.1 $RPM_BUILD_ROOT%{_mandir}/man1/ansible-playbook.1
cp -a library/* $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc VERSION *.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hosts
%attr(755,root,root) %{_bindir}/ansible
%attr(755,root,root) %{_bindir}/ansible-doc
%attr(755,root,root) %{_bindir}/ansible-playbook
%attr(755,root,root) %{_bindir}/ansible-pull
%{_mandir}/man1/ansible.1*
%{_mandir}/man1/ansible-playbook.1*
%{_datadir}/%{name}
%{py_sitescriptdir}/ansible
%{py_sitescriptdir}/ansible-%{version}-*.egg-info
