# Changes in Version 2

## Summary of breaking changes
- Switched to Docker Community Edition (uses overlay as the default storage driver).
- Use `/etc/docker/daemon.json` for configuration instead of modifying the package's systemd service.
- Removed `docker_repo_version` parameter.
