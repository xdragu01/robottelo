"""Global Configurations for py.test runner"""
import pytest

pytest_plugins = [
    # Plugins
    'pytest_plugins.disable_rp_params',
    'pytest_plugins.fixture_markers',
    'pytest_plugins.infra_dependent_markers',
    'pytest_plugins.issue_handlers',
    'pytest_plugins.logging_hooks',
    'pytest_plugins.manual_skipped',
    'pytest_plugins.marker_deselection',
    'pytest_plugins.markers',
    'pytest_plugins.metadata_markers',
    'pytest_plugins.settings_skip',
    'pytest_plugins.rerun_rp.rerun_rp',
    'pytest_plugins.fspath_plugins',
    'pytest_plugins.fixture_collection',
    # Fixtures
    'pytest_fixtures.core.broker',
    'pytest_fixtures.core.contenthosts',
    'pytest_fixtures.core.reporting',
    'pytest_fixtures.core.sys',
    'pytest_fixtures.core.upgrade',
    'pytest_fixtures.core.xdist',
    'pytest_fixtures.core.ui',
    # Component Fixtures
    'pytest_fixtures.component.activationkey',
    'pytest_fixtures.component.ansible',
    'pytest_fixtures.component.architecture',
    'pytest_fixtures.component.computeprofile',
    'pytest_fixtures.component.contentview',
    'pytest_fixtures.component.domain',
    'pytest_fixtures.component.host',
    'pytest_fixtures.component.hostgroup',
    'pytest_fixtures.component.http_proxy',
    'pytest_fixtures.component.katello_certs_check',
    'pytest_fixtures.component.lce',
    'pytest_fixtures.component.maintain',
    'pytest_fixtures.component.os',
    'pytest_fixtures.component.oscap',
    'pytest_fixtures.component.partition_table',
    'pytest_fixtures.component.provision_azure',
    'pytest_fixtures.component.provision_gce',
    'pytest_fixtures.component.provision_libvirt',
    'pytest_fixtures.component.provision_pxe',
    'pytest_fixtures.component.provisioning_template',
    'pytest_fixtures.component.puppet',
    'pytest_fixtures.component.repository',
    'pytest_fixtures.component.rh_cloud',
    'pytest_fixtures.component.satellite_auth',
    'pytest_fixtures.component.settings',
    'pytest_fixtures.component.smartproxy',
    'pytest_fixtures.component.subnet',
    'pytest_fixtures.component.subscription',
    'pytest_fixtures.component.taxonomy',
    'pytest_fixtures.component.templatesync',
    'pytest_fixtures.component.user_role',
]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)
