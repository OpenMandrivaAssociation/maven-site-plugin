Name:           maven-site-plugin
Version:        2.2
Release:        2
Summary:        Maven Site Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-site-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Patch0:         add-servlet-dep.patch

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: maven
BuildRequires: maven-plugin-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: plexus-maven-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-doxia
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-doxia-tools
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-plugin-cobertura
BuildRequires: jetty
Requires: maven2
Requires: jetty
Requires: java
Requires: jpackage-utils
Requires: maven-doxia-tools
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

Provides:       maven2-plugin-site = %{version}-%{release}
Obsoletes:      maven2-plugin-site <= 0:2.0.8

%description
The Maven Site Plugin is a plugin that generates a site for the current project.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-local \
        -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap org.apache.maven.plugins maven-site-plugin %{version} JPP maven-site-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

