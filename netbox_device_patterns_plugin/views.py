"""
Views for NetBox Device Patterns Plugin.

For more information on NetBox views, see:
https://docs.netbox.dev/en/stable/plugins/development/views/

For generic view classes, see:
https://docs.netbox.dev/en/stable/development/views/


from netbox.views import generic

from . import filtersets, forms, models, tables


class DevicepatternsView(generic.ObjectView):
    queryset = models.Devicepatterns.objects.all()


class DevicepatternsListView(generic.ObjectListView):
    queryset = models.Devicepatterns.objects.all()
    table = tables.DevicepatternsTable
    filterset = filtersets.DevicepatternsFilterSet


class DevicepatternsEditView(generic.ObjectEditView):
    queryset = models.Devicepatterns.objects.all()
    form = forms.DevicepatternsForm


class DevicepatternsDeleteView(generic.ObjectDeleteView):
    queryset = models.Devicepatterns.objects.all()

"""

# copilot

from netbox.views import generic
from .models import (
    Project,
    EndpointDefinition,
    EndpointInstance,
    PhysicalLink,
)
from .forms import (
    ProjectForm,
    EndpointDefinitionForm,
    EndpointInstanceForm,
    PhysicalLinkForm,
)


#
# Project Views
#

class ProjectListView(generic.ObjectListView):
    queryset = Project.objects.all()
    table = None  # you will define tables later


class ProjectView(generic.ObjectView):
    queryset = Project.objects.all()


class ProjectEditView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = ProjectForm


class ProjectDiagramView(generic.ObjectView):
    queryset = Project.objects.all()
    template_name = 'yourplugin/project_diagram.html'


#
# Endpoint Definition Views
#

class EndpointDefinitionListView(generic.ObjectListView):
    queryset = EndpointDefinition.objects.all()
    table = None


class EndpointDefinitionView(generic.ObjectView):
    queryset = EndpointDefinition.objects.all()


class EndpointDefinitionEditView(generic.ObjectEditView):
    queryset = EndpointDefinition.objects.all()
    form = EndpointDefinitionForm


class EndpointDefinitionCloneView(generic.ObjectEditView):
    queryset = EndpointDefinition.objects.all()
    form = EndpointDefinitionForm
    template_name = 'yourplugin/endpointdefinition_clone.html'


#
# Endpoint Instance Views
#

class EndpointInstanceListView(generic.ObjectListView):
    queryset = EndpointInstance.objects.all()
    table = None


class EndpointInstanceView(generic.ObjectView):
    queryset = EndpointInstance.objects.all()


class EndpointInstanceEditView(generic.ObjectEditView):
    queryset = EndpointInstance.objects.all()
    form = EndpointInstanceForm


#
# Physical Link Views
#

class PhysicalLinkEditView(generic.ObjectEditView):
    queryset = PhysicalLink.objects.all()
    form = PhysicalLinkForm


