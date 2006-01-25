%define rubylibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')
%define _pbuild %{_builddir}/%{name}-%{version}
%define puppetroot /home/luke/svn/puppet/trunk
%define confdir %{puppetroot}/conf/redhat
%define pkgdir %{puppetroot}/pkg

Summary: A network tool for managing many disparate systems
Name: puppet
Version: 0.11.2
Release: 1
License: GPL
Group: System Environment/Base

URL: http://reductivelabs.com/projects/puppet/
Source: http://reductivelabs.com/downloads/puppet/%{name}-%{version}.tgz
Source1: client.init
Source2: client.sysconfig
Source3: client.cron
Source4: server.sysconfig
Source5: server.init
Source6: fileserver.conf

Vendor: Reductive Labs
Packager: Duane Griffin <d.griffin@psenterprise.com>

Requires: ruby >= 1.8.1
Requires: facter >= 1.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArchitectures: noarch

%description
Puppet lets you centrally manage every important aspect of your system using a 
cross-platform specification language that manages all the separate elements 
normally aggregated in different files, like users, cron jobs, and hosts, 
along with obviously discrete elements like packages, services, and files.

%package server
Group: System Environment/Base
Summary: Server for the puppet system management tool.
Requires: puppet = %{version}-%{release}

%description server
Provides the central puppet server daemon which provides manifests to clients.
The server can also function as a certificate authority and file server.

%prep
%setup -q

%{__cp} -p %{confdir}/* .

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_sbindir}
%{__install} -d -m0755 %{buildroot}%{rubylibdir}
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/puppet/manifests
%{__install} -d -m0755 %{buildroot}%{_docdir}/%{name}-%{version}
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/puppet
%{__install} -Dp -m0755 %{_pbuild}/bin/* %{buildroot}%{_sbindir}
%{__install} -Dp -m0644 %{_pbuild}/lib/puppet.rb %{buildroot}%{rubylibdir}/puppet.rb
%{__cp} -a %{_pbuild}/lib/puppet %{buildroot}%{rubylibdir}
%{__install} -Dp -m0644 client.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppet
%{__install} -Dp -m0755 client.init %{buildroot}%{_initrddir}/puppet
%{__install} -Dp -m0644 client.cron %{buildroot}%{_sysconfdir}/cron.hourly/puppet.cron
%{__install} -Dp -m0644 server.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/puppetmaster
%{__install} -Dp -m0755 server.init %{buildroot}%{_initrddir}/puppetmaster
%{__install} -Dp -m0644 fileserver.conf %{buildroot}%{_sysconfdir}/puppet/fileserver.conf

%files
%defattr(-, root, root, 0755)
%{_sbindir}/puppet
%{_sbindir}/puppetd
%{rubylibdir}/*
%{_localstatedir}/puppet
%config %{_initrddir}/puppet
%config %{_sysconfdir}/cron.hourly/puppet.cron
%config(noreplace) %{_sysconfdir}/sysconfig/puppet
%doc CHANGELOG COPYING LICENSE README TODO examples
%exclude %{_sbindir}/puppetdoc

%files server
%{_sbindir}/puppetmasterd
%config %{_initrddir}/puppetmaster
%config(noreplace) %{_sysconfdir}/puppet/*
%config(noreplace) %{_sysconfdir}/sysconfig/puppetmaster
%config(noreplace) %{_sysconfdir}/puppet/fileserver.conf
%{_sbindir}/cf2puppet
%{_sbindir}/puppetca

%post
touch %{_localstatedir}/log/puppet.log
/sbin/chkconfig --add puppet
exit 0

%post server
touch %{_localstatedir}/log/puppetmaster.log
touch %{_localstatedir}/log/puppetmaster-http.log
/sbin/chkconfig --add puppetmaster

%preun
if [ "$1" = 0 ] ; then
	/sbin/service puppet stop > /dev/null 2>&1
	/sbin/chkconfig --del puppet
fi

%preun server
if [ "$1" = 0 ] ; then
	/sbin/service puppetmaster stop > /dev/null 2>&1
	/sbin/chkconfig --del puppetmaster
fi

%postun server
if [ "$1" -ge 1 ]; then
	 /sbin/service puppetmaster condrestart > /dev/null 2>&1
fi

%clean
%{__rm} -rf %{buildroot}

%changelog
* Tue Jan 17 2006 David Lutterkort <dlutter@redhat.com> - 0.11.0-1
- Rebuild

* Thu Jan 12 2006 David Lutterkort <dlutter@redhat.com> - 0.10.2-1
- Updated for 0.10.2 Fixed minor kink in how Source is given

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-3
- Added basic fileserver.conf

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-1
- Updated. Moved installation of library files to sitelibdir. Pulled 
initscripts into separate files. Folded tools rpm into server

* Thu Nov 24 2005 Duane Griffin <d.griffin@psenterprise.com>
- Added init scripts for the client
* Wed Nov 23 2005 Duane Griffin <d.griffin@psenterprise.com>
- First packaging
