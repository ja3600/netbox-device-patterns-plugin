"""
NetBox Device Patterns Plugin

Plugin configuration for NetBox Device Patterns Plugin.

For a complete list of PluginConfig attributes, see:
https://docs.netbox.dev/en/stable/plugins/development/#pluginconfig-attributes
"""

__author__ = """John Alberti"""
__email__ = "pyman2112@outlook.com"
__version__ = "0.1.0"


from netbox.plugins import PluginConfig


class DevicepatternsConfig(PluginConfig):
    name = "netbox_device_patterns_plugin"
    verbose_name = "NetBox Device Patterns Plugin"
    description = "NetBox plugin for Device Patterns."
    author= "John Alberti"
    author_email = "pyman2112@outlook.com"
    version = __version__
    base_url = "netbox_device_patterns_plugin"
    min_version = "4.5.0"
    max_version = "4.5.99"
    graphql_schema = "graphql.schema"


config = DevicepatternsConfig
