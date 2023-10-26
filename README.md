Docker
======

[![Actions Status](https://github.com/ome/ansible-role-docker/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-docker/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-docker-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/docker/)

Setup Docker, provides options for using an advanced storage or networking configuration.
Installs the latest official upstream Docker (Community Edition).

This role should work with RedHat Enterprise Linux 7, but [this is not supported by Docker](https://docs.docker.com/install/linux/docker-ee/rhel/).

If you want the distribution supplied Docker package do not use this role.


Role Variables
--------------

Optional variables:
- `docker_version`: Install a particular version of docker, e.g. `17.12.1.ce-1.el7.centos`, default current
- `docker_groupmembers`: A list of users who will be added to the `docker` system group, allows docker to be run without sudo
- `docker_use_ipv4_nic_mtu`: Force Docker to use the MTU set by the main IPV4 interface. This may be necessary on virtualised hosts, see comment in `defaults/main.yml`.
- `docker_additional_options`: Dictionary of additional Docker configuration options.
- `docker_use_custom_storage`: If `True` use a custom storage configuration, default `False`
- `docker_use_custom_network`: If `True` use a custom network configuration, default `False`
- `docker_systemd_setup`: Set this to False to disable automatic systemd configuration, default `False`.
  You may wish to use this when building virtualisation images.
- `docker_repo_force_releasever`: The repo config uses the `$releasever` variables. On some systems this may not work, if necessary you can forcibly override it by setting this variable.


### Custom storage

If `docker_use_custom_storage` is `True` thin-pool logical volumes will be created for Docker, and a separate logical volume will be created for the Docker volume (`/var/lib/docker`).

- `docker_basefs`: Filesystem to use for the Docker containers (default xfs)
- `docker_lvfilesystem`: Filesystem for the Docker volume (default xfs)
- `docker_lvopts`: Additional arguments to be used when creating logical volumes

The following variables must be defined when using custom storage:

- `docker_vgname`: LVM volume group for the logical volumes
- `docker_poolsize`: Size of the Docker thin-pool partition
- `docker_metadatasize`: Size of the Docker thin-pool metadata partition (try 1% of the poolsize)
- `docker_volumesize`: Size of the Docker volume

If `docker_use_custom_storage` is `False` you may wish to mount `/var/lib/docker` on a separate partition or volume before applying this role.


### Custom networking

If `docker_use_custom_network` is `True` a custom network bridge will be used, this must be created outside of this role.
The following variables must be defined:

- `docker_bridge_name`: The name of a custom network bridge for docker
- `docker_bridge_ips`: The custom IP range that docker should use for allocating IPs


Dependencies
------------

Depends on lvm-partition.


Development
-----------

This role is partially tested by Travis-CI, which requires running Docker-in-Docker.
When testing changes you should therefore run a full test using molecule with the Vagrant driver as part of any review:

    molecule test --driver vagrant


Example Playbook
----------------

Simple example (uses default storage overlay driver):

    - hosts: localhost
      roles:
        - role: ome.docker

Example using the default storage driver, with a dedicated logical volume for docker:

    - hosts: localhost
      roles:
        - role: ome.lvm_partition
          lvm_lvname: var_lib_docker
          lvm_lvmount: /var/lib/docker
          lvm_lvsize: 100g
          lvm_lvfilesystem: ext4
        - role: ome.docker

Advanced example using custom storage and listening on external port 4243 (insecure).
The LVM volume group `VolGroup00` must already exist:

    - hosts: localhost
      roles:
        - role: ome.docker
          docker_use_ipv4_nic_mtu: True
          docker_use_custom_storage: True
          docker_vgname: VolGroup00
          docker_poolsize: 10g
          docker_metadatasize: 100m
          docker_volumesize: 5g
          docker_groupmembers: [centos]
          docker_additional_options:
            hosts:
              - tcp://0.0.0.0:4243
              - unix:///var/run/docker.sock


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
