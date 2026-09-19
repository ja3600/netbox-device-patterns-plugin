"""
URL patterns for NetBox Device Patterns Plugin.

For more information on URL routing, see:
https://docs.netbox.dev/en/stable/plugins/development/views/#url-registration

For Django URL patterns, see:
https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views

"""urlpatterns = (
    path("device-patternss/", views.DevicepatternsListView.as_view(), name="devicepatterns_list"),
    path("device-patternss/add/", views.DevicepatternsEditView.as_view(), name="devicepatterns_add"),
    path("device-patternss/<int:pk>/", views.DevicepatternsView.as_view(), name="devicepatterns"),
    path("device-patternss/<int:pk>/edit/", views.DevicepatternsEditView.as_view(), name="devicepatterns_edit"),
    path("device-patternss/<int:pk>/delete/", views.DevicepatternsDeleteView.as_view(), name="devicepatterns_delete"),
    path(
        "device-patternss/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="devicepatterns_changelog",
        kwargs={"model": models.Devicepatterns},
    ),
)
"""

#copilot

from django.urls import path
from . import views

urlpatterns = [

    # Project
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/add/', views.ProjectEditView.as_view(), name='project_add'),
    path('projects/<int:pk>/', views.ProjectView.as_view(), name='project'),
    path('projects/<int:pk>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
    path('projects/<int:pk>/diagram/', views.ProjectDiagramView.as_view(), name='project_diagram'),

    # Endpoint Definitions
    path('definitions/', views.EndpointDefinitionListView.as_view(), name='endpointdefinition_list'),
    path('definitions/add/', views.EndpointDefinitionEditView.as_view(), name='endpointdefinition_add'),
    path('definitions/<int:pk>/', views.EndpointDefinitionView.as_view(), name='endpointdefinition'),
    path('definitions/<int:pk>/edit/', views.EndpointDefinitionEditView.as_view(), name='endpointdefinition_edit'),
    path('definitions/<int:pk>/clone/', views.EndpointDefinitionCloneView.as_view(), name='endpointdefinition_clone'),

    # Endpoint Instances
    path('instances/', views.EndpointInstanceListView.as_view(), name='endpointinstance_list'),
    path('instances/add/', views.EndpointInstanceEditView.as_view(), name='endpointinstance_add'),
    path('instances/<int:pk>/', views.EndpointInstanceView.as_view(), name='endpointinstance'),
    path('instances/<int:pk>/edit/', views.EndpointInstanceEditView.as_view(), name='endpointinstance_edit'),

    # Physical Links
    path('links/add/', views.PhysicalLinkEditView.as_view(), name='physicallink_add'),
    path('links/<int:pk>/edit/', views.PhysicalLinkEditView.as_view(), name='physicallink_edit'),
]
