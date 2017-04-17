import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('docker-inactive')


def test_docker_installed(Command, Sudo):
    with Sudo():
        cmd = Command('docker info')
    assert cmd.rc == 1
    assert cmd.stderr.startswith('Cannot connect to the Docker daemon')
