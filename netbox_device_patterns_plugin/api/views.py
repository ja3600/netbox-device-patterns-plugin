"""
API viewsets for NetBox Device Patterns Plugin.

For more information on NetBox REST API viewsets, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#viewsets

For Django REST Framework viewsets, see:
https://www.django-rest-framework.org/api-guide/viewsets/
"""

from netbox.api.viewsets import NetBoxModelViewSet

from ..models import Devicepatterns
from .serializers import DevicepatternsSerializer


class DevicepatternsViewSet(NetBoxModelViewSet):
    queryset = Devicepatterns.objects.all()
    serializer_class = DevicepatternsSerializer

