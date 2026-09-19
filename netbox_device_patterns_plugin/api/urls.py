"""
API URL patterns for NetBox Device Patterns Plugin.

For more information on NetBox REST API routing, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#routers

For Django REST Framework routers, see:
https://www.django-rest-framework.org/api-guide/routers/
"""

from netbox.api.routers import NetBoxRouter

from .views import DevicepatternsViewSet

app_name = "netbox_device_patterns_plugin"

router = NetBoxRouter()
router.register("device-patternss", DevicepatternsViewSet)

urlpatterns = router.urls

