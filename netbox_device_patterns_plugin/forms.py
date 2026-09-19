"""
Forms for NetBox Device Patterns Plugin.

For more information on NetBox forms, see:
https://docs.netbox.dev/en/stable/plugins/development/forms/


from netbox.forms import NetBoxModelForm

from .models import Devicepatterns


class DevicepatternsForm(NetBoxModelForm):
    class Meta:
        model = Devicepatterns
        fields = ("name", "tags")
"""

from django import forms
from .models import (
    Project,
    EndpointDefinition,
    EndpointInstance,
    PhysicalLink,
)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'site', 'tags']


class EndpointDefinitionForm(forms.ModelForm):
    interfaces = forms.JSONField(
        required=False,
        help_text="List of interface definitions with nested services."
    )

    class Meta:
        model = EndpointDefinition
        fields = [
            'name',
            'manufacturer',
            'model',
            'role',
            'category',
            'interfaces',
            'image',
            'tags',
        ]


class EndpointInstanceForm(forms.ModelForm):
    overrides = forms.JSONField(
        required=False,
        help_text="Instance-level overrides for interfaces/services."
    )

    class Meta:
        model = EndpointInstance
        fields = [
            'name',
            'definition',
            'project',
            'device',
            'overrides',
            'tags',
        ]


class PhysicalLinkForm(forms.ModelForm):
    class Meta:
        model = PhysicalLink
        fields = [
            'endpoint',
            'endpoint_interface_name',
            'device',
            'device_interface',
        ]


