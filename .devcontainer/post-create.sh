#!/usr/bin/env bash
set -e

echo "🚀 Setting up NetBox development environment..."

# Clone NetBox Docker
git clone https://github.com/ja3600/netbox-docker.git /workspaces/netbox-docker

# Install your plugin into NetBox Docker's plugin directory
mkdir -p /workspaces/netbox-docker/plugins
# ln -s /workspaces/netbox-device-patterns-plugin \
#       /workspaces/netbox-docker/plugins/netbox-device-patterns-plugin

# # Enable plugin in NetBox configuration
# cat <<EOF >> /workspaces/netbox-docker/configuration/plugins.py
# PLUGINS = [
#     "netbox_device_patterns_plugin",
# ]
# EOF

echo "🔧 Starting NetBox stack..."
cd /workspaces/netbox-docker
docker compose pull
docker compose up -d

echo "🎉 NetBox is running at: http://localhost:8000"
