#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (missing in sdist)

Summary:	Tools for Tidelift by jaraco
Summary(pl.UTF-8):	Narzędzia do serwisu Tidelift autorstwa jaraco
Name:		python3-jaraco.tidelift
Version:	1.5.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco.tidelift/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco.tidelift/jaraco.tidelift-%{version}.tar.gz
# Source0-md5:	6a95586094fafed2703efdbec0ffc951
URL:		https://pypi.org/project/jaraco.tidelift/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-autocommand
BuildRequires:	python3-importlib_resources >= 1.6
BuildRequires:	python3-keyring
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-black >= 0.3.7
BuildRequires:	python3-pytest-checkdocs >= 2.4
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-enabler >= 1.0.1
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-pytest-mypy >= 0.9.1
BuildRequires:	python3-requests-toolbelt
#BuildRequires:	python3-types-docutils
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 8.2
#BuildRequires:	python3-jaraco.packaging >= 9  # when available
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools for Tidelift by jaraco.

%description -l pl.UTF-8
Narzędzia do serwisu Tidelift autorstwa jaraco.

%package apidocs
Summary:	API documentation for Python jaraco.tidelift module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jaraco.tidelift
Group:		Documentation

%description apidocs
API documentation for Python jaraco.tidelift module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jaraco.tidelift.

%prep
%setup -q -n jaraco.tidelift-%{version}

# stub for setuptools
cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=... \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/jaraco/tidelift
%{py3_sitescriptdir}/jaraco.tidelift-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
