#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	-
Summary(pl.UTF-8):	-
Name:		xl2tpd
Version:	1.2.8
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.xelerance.com/wp-content/uploads/software/xl2tpd/%{name}-%{version}.tar.gz
# Source0-md5:	8748ac5e2f5289963d9a908eede546b5
URL:		http://www.xelerance.com/software/xl2tpd/
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%endif
#BuildRequires:	-
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
Requires:	ppp
#Provides:	-
#Provides:	group(foo)
#Provides:	user(foo)
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xl2tpd is an implementation of the Layer 2 Tunnelling Protocol (RFC
2661). L2TP allows you to tunnel PPP over UDP. Some ISPs use L2TP to
tunnel user sessions from dial-in servers (modem banks, ADSL DSLAMs)
to back-end PPP servers. Another important application is Virtual
Private Networks where the IPsec protocol is used to secure the L2TP
connection (L2TP/IPsec, RFC 3193). The L2TP/IPsec protocol is mainly
used by Windows and Mac OS X clients. On Linux, xl2tpd can be used in
combination with IPsec implementations such as Openswan.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
%if %{with initscript}
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
%endif
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with initscript}
%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS CHANGES TODO
%attr(755,root,root) %{_bindir}/p*
%attr(755,root,root) %{_sbindir}/xl*
%{_mandir}/man[158]/*

%if 0
# if _sysconfdir != /etc:
#%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_datadir}/%{name}
%endif

# initscript and its config
%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif

#%{_examplesdir}/%{name}-%{version}

%if %{with subpackage}
%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%endif
