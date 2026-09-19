# copilot

from django.contrib import admin
from .models import (
    Project,
    EndpointDefinition,
    EndpointInstance,
    PhysicalLink,
    EndpointDefinitionTaggedItem,
    EndpointInstanceTaggedItem,
    ProjectTaggedItem,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')
    search_fields = ('name',)
    list_filter = ('site',)


@admin.register(EndpointDefinition)
class EndpointDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'model', 'role', 'category')
    search_fields = ('name', 'manufacturer', 'model')
    list_filter = ('role', 'category')
    filter_horizontal = ('tags',)


@admin.register(EndpointInstance)
class EndpointInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition', 'project', 'device')
    search_fields = ('name',)
    list_filter = ('project', 'definition')
    filter_horizontal = ('tags',)


@admin.register(PhysicalLink)
class PhysicalLinkAdmin(admin.ModelAdmin):
    list_display = (
        'endpoint',
        'endpoint_interface_name',
        'device',
        'device_interface',
    )
    search_fields = ('endpoint__name', 'endpoint_interface_name')
    list_filter = ('device',)
