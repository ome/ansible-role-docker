import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('docker')


def test_service_running_and_enabled(Service):
    assert Service('docker').is_running
    assert Service('docker').is_enabled


def test_docker_info(Command, Sudo):
    with Sudo():
        Command.check_output('docker info')


def test_docker_socket_unprivileged(Command, Sudo):
    with Sudo('test'):
        r = Command('docker info')
    assert r.rc > 0
    assert 'permission denied' in r.stderr


def test_docker_tcp_unprivileged(Command, Sudo):
    with Sudo('test'):
        Command.check_output('DOCKER_HOST=tcp://127.0.0.1:4243 docker info')


def test_docker_run(Command, Sudo):
    with Sudo():
        out = Command.check_output('docker run busybox id')
    assert out == 'uid=0(root) gid=0(root) groups=10(wheel)'
