import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('xdockerx')


def test_service_running_and_enabled(host):
    assert host.service('docker').is_running
    assert host.service('docker').is_enabled


def test_docker_info(host):
    with host.sudo():
        host.command.check_output('docker info')


def test_docker_socket_unprivileged(host):
    with host.sudo('test'):
        r = host.command('docker info')
    assert r.rc > 0
    assert 'permission denied' in r.stdout


def test_docker_tcp_unprivileged(host):
    with host.sudo('test'):
        host.command.check_output(
            'DOCKER_HOST=tcp://127.0.0.1:4243 docker info')


def test_docker_run(host):
    with host.sudo():
        out = host.command.check_output('docker run busybox id')
    assert out == 'uid=0(root) gid=0(root) groups=0(root),10(wheel)'


def test_docker_package(host):
    assert host.package('docker-ce').is_installed
    assert not host.package('docker').is_installed
