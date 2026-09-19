"""
Navigation menu items for NetBox Device Patterns Plugin.

For more information on navigation menus, see:
https://docs.netbox.dev/en/stable/plugins/development/navigation/
"""

from netbox.plugins import PluginMenuButton, PluginMenuItem

plugin_buttons = [
    PluginMenuButton(
        link="plugins:netbox_device_patterns_plugin:devicepatterns_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_device_patterns_plugin:devicepatterns_list",
        link_text="Device Patterns",
        buttons=plugin_buttons,
    ),
)
