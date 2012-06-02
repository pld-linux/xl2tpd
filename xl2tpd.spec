Summary:	Layer 2 Tunnelling Protocol Daemon (RFC 2661)
Summary(pl.UTF-8):	Demon protokołu tunelowania warstwy 2 (L2TP, RFC 2661)
Name:		xl2tpd
Version:	1.3.0
Release:	2
License:	GPL v2
Group:		Networking/Daemons
#Source0Download: http://www.xelerance.com/services/software/xl2tpd/
Source0:	http://www.xelerance.com/wp-content/uploads/software/xl2tpd/%{name}-%{version}.tar.gz
# Source0-md5:	28264284552c442b24cf421755a2bb48
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Source3:	%{name}.tmpfiles
Patch0:		%{name}-build_flags.patch
Patch1:		%{name}-control_crash.patch
URL:		http://www.xelerance.com/software/xl2tpd/
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:  libpcap-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	ppp
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

%description -l pl.UTF-8
xl2tpd to implementacja L2TP (Layer 2 Tunnelling Protocol - protokołu
tunelowania warstwy 2, wg RFC 2661). L2TP pozwala na tunelowanie PPP
po UDP. Niektórzy ISP wykorzystują L2TP do tunelowania sesji
użytkowników z serwerów wdzwanianych (banki modemowe, ADSL DSLAM) na
serwery backendowe PPP. Inne ważne zastosowanie to wirtualne sieci
prywatne (VPN), gdzie protokół IPsec jest wykorzystywany do
zabezpieczenia połączenia L2TP (L2TP/IPsec, RFC 3193). Protokół
L2TP/IPsec jest wykorzystywany głównie przez klientów Windows i Mac OS
X. Na Linuksie xl2tpd może być wykorzystywany w połączeniu z
implementacjami IPsec, takimi jak Openswan.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPMCFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
		$RPM_BUILD_ROOT/%{_sysconfdir}/%{name} \
		$RPM_BUILD_ROOT/var/run/%{name} \
		$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

install doc/l2tp-secrets.sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/l2tp-secrets
install doc/l2tpd.conf.sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/xl2tpd.conf

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
	rm -f /var/run/xl2tpd/l2tp-control 2>/dev/null || :
fi

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS CHANGES README.xl2tpd TODO contrib/pfc.README
%attr(755,root,root) %{_bindir}/pfc
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}-control
%{_mandir}/man1/pfc.1*
%{_mandir}/man5/l2tp-secrets.5*
%{_mandir}/man5/xl2tpd.conf.5*
%{_mandir}/man8/xl2tpd.8*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/l2tp-secrets
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
/usr/lib/tmpfiles.d/%{name}.conf
%dir /var/run/%{name}
