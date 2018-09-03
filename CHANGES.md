# Changes in Version 3

## Summary of breaking changes
- Removed support for installing distribution docker
- Removed `docker_install_upstream` parameter


# Changes in Version 2

## Summary of breaking changes
- Switched to Docker Community Edition (uses overlay as the default storage driver).
- Use `/etc/docker/daemon.json` for configuration instead of modifying the package's systemd service.
- Removed `docker_repo_version` parameter.
