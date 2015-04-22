%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name redhat_access
%global rubyabi 1.9.1
%global foreman_dir /usr/share/foreman
%global foreman_bundlerd_dir %foreman_dir/bundler.d
%global foreman_assets_dir %foreman_dir/public/assets
%global rubygem_redhat_access_dir %{gem_dir}/gems/%{gem_name}-%{version}

%if "%{?scl}" == "ruby193"
    %global scl_rake /usr/bin/ruby193-rake
%else
    %global scl_rake /usr/bin/rake
%endif

Name: %{?scl_prefix}rubygem-foreman-%{gem_name}
Version: 0.2.0
Release: 1%{?dist}
Summary: Foreman engine to access Red Hat knowledge base and manage support cases.
Group: Development/Languages
License: GPLv2+
URL: https://github.com/redhataccess/foreman-plugin
Source0: %{gem_name}-%{version}.gem


Requires: foreman => 1.5.0

Requires: %{?scl_prefix}ruby(abi)
Requires: %{?scl_prefix}rubygems
Requires: %{?scl_prefix}rubygem(rails)
Requires: %{?scl_prefix}rubygem-angular-rails-templates >= 0.0.4
Requires: %{?scl_prefix}rubygem-redhat_access_lib >= 0.0.2

BuildRequires: %{?scl_prefix}rubygem-angular-rails-templates >= 0.0.4
BuildRequires: %{?scl_prefix}ruby(abi)
BuildRequires: %{?scl_prefix}rubygems
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}rubygem(rake)
BuildRequires: %{?scl_prefix}rubygem(sass-rails)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix}rubygem(jquery-rails)
BuildRequires: %{?scl_prefix}rubygem(uglifier)
BuildRequires: %{?scl_prefix}rubygem(haml-rails)
BuildRequires: %{?scl_prefix}rubygem(therubyracer)


BuildArch: noarch

Provides: %{?scl_prefix}rubygem(foreman-%{gem_name}) = %{version}

%description
Foreman engine to access Red Hat knowledge base search

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}

%build
mkdir -p .%{gem_dir}

# precompile JavaScript assets...
%{scl_rake} assets:precompile:engine --trace

# Create our gem
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

# install our gem locally, to be move into buildroot in %%install
%{?scl:scl enable %{scl} "}
gem install --local --no-wrappers --install-dir .%{gem_dir} --force --no-rdoc --no-ri %{gem_name}-%{version}.gem
%{?scl:"}

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{foreman_bundlerd_dir}
mkdir -p %{buildroot}%{foreman_assets_dir}
mkdir -p %{buildroot}/etc/redhat_access
mkdir -p %{buildroot}/etc/pam.d
mkdir -p %{buildroot}/etc/security/console.apps
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/bin

cp -pa .%{gem_dir}/* %{buildroot}%{gem_dir}/

cat <<GEMFILE > %{buildroot}%{foreman_bundlerd_dir}/%{gem_name}.rb
gem 'redhat_access'
GEMFILE

# add link to precompiled assets
ln -s %{rubygem_redhat_access_dir}/public/assets/redhat_access %{buildroot}%{foreman_assets_dir}/redhat_access

# copy sos report functions
cp -pa .%{rubygem_redhat_access_dir}/script/sos_reports/foreman_sosreport.pam %{buildroot}/etc/pam.d/foreman-sosreport
cp -pa .%{rubygem_redhat_access_dir}/script/sos_reports/foreman_sosreport_console.apps %{buildroot}/etc/security/console.apps/foreman-sosreport
cp -pa .%{rubygem_redhat_access_dir}/script/sos_reports/foreman_sosreport_wrapper.py %{buildroot}/usr/sbin/foreman-sosreport-wrapper
chmod 755 %{buildroot}/usr/sbin/foreman-sosreport-wrapper
ln -s /usr/bin/consolehelper %{buildroot}/usr/bin/foreman-sosreport
cp -pa .%{rubygem_redhat_access_dir}/config/config.yml.example %{buildroot}/etc/redhat_access/config.yml

%files
%defattr(-,root,root,-)
%{gem_dir}
%{foreman_bundlerd_dir}/%{gem_name}.rb
%{foreman_assets_dir}/redhat_access
/etc/redhat_access
/etc/pam.d
/etc/security/console.apps
/usr/sbin
/usr/bin

%posttrans
/usr/sbin/foreman-rake db:migrate >/dev/null 2>&1

%changelog
* Mon Dec 12 2014 Lindani Phiri <lindani@redhat.com> - 0.0.7-1
- Add proactive support
- Resolves: bz1131538
- Resolves: bz1145742

* Wed May 14 2014 Rex White <rexwhite@redhat.com> - 0.0.4-1
- Resolves: bz1084590
- Updated for UX comments

* Wed May 14 2014 Rex White <rexwhite@redhat.com> - 0.0.3-1
- Resolves: bz1084590

* Wed May 14 2014 Rex White <rexwhite@redhat.com> - 0.0.3-1
- Version: 0.0.3-1
- Fixed rake asset precompilation to work on RHEL 7

* Tue Apr 29 2014 Rex White <rexwhite@redhat.com>
- Renamed spec file
- Added SOS report files

* Tue Apr 22 2014 Rex White <rexhwite@redhat.com>
- Fixed asset pre-compile issues
- Fixed incorrect foreman path variables

* Thu Apr 3 2014 Rex White <rexwhite@redhat.com>
- Initial package

