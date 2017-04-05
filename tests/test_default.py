import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_service_running_and_enabled(Service):
    assert Service('docker').is_running
    assert Service('docker').is_enabled


def test_docker_info(Command, Sudo):
    with Sudo():
        Command.check_output('docker info')
