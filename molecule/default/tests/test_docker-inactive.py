import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('docker-inactive')


def test_docker_installed(host):
    with host.sudo():
        cmd = host.command('docker info')
    assert cmd.rc == 1
    assert 'ERROR: Cannot connect to the Docker daemon' in cmd.stdout
