"""
Models for NetBox Device Patterns Plugin.

For more information on NetBox models, see:
https://docs.netbox.dev/en/stable/plugins/development/models/

For NetBox model features (tags, custom fields, change logging, etc.), see:
https://docs.netbox.dev/en/stable/development/models/#netbox-model-features
"""

## cookiecutter
'''
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


class Devicepatterns(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = "netbox_device_patterns_plugin"
        ordering = ("name",)
        verbose_name_plural = "Devicepatternss"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_device_patterns_plugin:devicepatterns", args=[self.pk])
'''

from django.contrib.postgres.fields import JSONField
from django.db import models
from netbox.models import PrimaryModel
from netbox.tags.models import TaggedItem
from utilities.querysets import RestrictedQuerySet

# code created by copilot

class Project(PrimaryModel):
    """
    A design/implementation project (e.g., 'West Yard Control House').
    """
    name = models.CharField(max_length=100, unique=True)
    site = models.ForeignKey(
        'dcim.Site',
        on_delete=models.PROTECT,
        related_name='endpoint_projects',
        null=True,
        blank=True,
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class EndpointDefinition(PrimaryModel):
    """
    Template describing an endpoint type: interfaces + services + metadata.
    """
    ROLE_CHOICES = (
        ('rtu', 'RTU'),
        ('relay', 'Relay'),
        ('hmi', 'HMI'),
        ('ip_phone', 'IP Phone'),
        # extend as needed
    )

    CATEGORY_CHOICES = (
        ('scada', 'SCADA'),
        ('protection', 'Protection'),
        ('voice', 'Voice'),
        # extend as needed
    )

    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    # Structured definition of interfaces + services
    # Example:
    # [
    #   {
    #     "name": "eth0",
    #     "description": "SCADA NIC",
    #     "role": "scada",
    #     "services": [
    #       {"name": "DNP3", "protocol": "tcp", "port": 20000, "dscp": "CS2", "bandwidth_kbps": 64},
    #       {"name": "ICCP", "protocol": "tcp", "port": 102, "dscp": "CS3", "bandwidth_kbps": 128}
    #     ]
    #   },
    #   ...
    # ]
    interfaces = JSONField(default=list, blank=True)

    # Optional image (photo only, not used in diagrams)
    image = models.ImageField(upload_to='endpoint_definitions', blank=True, null=True)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class EndpointInstance(PrimaryModel):
    """
    A concrete endpoint in a project/site, inheriting from EndpointDefinition.
    """
    name = models.CharField(max_length=100)

    definition = models.ForeignKey(
        EndpointDefinition,
        on_delete=models.PROTECT,
        related_name='instances',
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='endpoints',
        null=True,
        blank=True,
    )

    # Optional mapping to a NetBox device (e.g., SEL-3505, Cisco IE3300)
    device = models.ForeignKey(
        'dcim.Device',
        on_delete=models.PROTECT,
        related_name='endpoint_instances',
        null=True,
        blank=True,
    )

    # Instance-level overrides + enable/disable state
    # Example:
    # {
    #   "interfaces": [
    #     {
    #       "name": "eth0",
    #       "services": [
    #         {"name": "DNP3", "enabled": True},
    #         {"name": "ICCP", "enabled": False, "dscp": "CS1"},
    #         {"name": "Telemetry", "enabled": True, "protocol": "udp", "port": 9000}
    #       ]
    #     },
    #     ...
    #   ]
    # }
    overrides = JSONField(default=dict, blank=True)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'project')

    def __str__(self):
        return self.name

    #
    # Effective structure helpers (definition + overrides merged)
    #

    def get_effective_interfaces(self):
        """
        Merge definition.interfaces with overrides to produce
        the effective interface + service structure for this instance.
        """
        from .utils import build_effective_interfaces
        return build_effective_interfaces(self.definition.interfaces, self.overrides)

    def get_effective_services(self):
        """
        Convenience wrapper to get services per interface.
        """
        interfaces = self.get_effective_interfaces()
        # flatten or return as-is depending on UI needs
        return interfaces


class PhysicalLink(PrimaryModel):
    """
    Physical connectivity: endpoint NIC -> device interface.
    Drives the project diagram edges.
    """
    endpoint = models.ForeignKey(
        EndpointInstance,
        on_delete=models.CASCADE,
        related_name='links',
    )

    endpoint_interface_name = models.CharField(max_length=64)

    device = models.ForeignKey(
        'dcim.Device',
        on_delete=models.PROTECT,
        related_name='endpoint_links',
    )

    device_interface = models.ForeignKey(
        'dcim.Interface',
        on_delete=models.PROTECT,
        related_name='endpoint_links',
        null=True,
        blank=True,
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['endpoint__name', 'endpoint_interface_name']

    def __str__(self):
        return f'{self.endpoint} {self.endpoint_interface_name} -> {self.device} {self.device_interface}'


#
# Optional: tag support (NetBox tagging)
#

class EndpointDefinitionTaggedItem(TaggedItem):
    content_object = models.ForeignKey(
        EndpointDefinition,
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class EndpointInstanceTaggedItem(TaggedItem):
    content_object = models.ForeignKey(
        EndpointInstance,
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class ProjectTaggedItem(TaggedItem):
    content_object = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )
