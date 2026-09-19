"""
Test cases for NetBox Device Patterns Plugin views.
"""

from django.urls import reverse

from ..models import Devicepatterns
from ..testing import PluginViewTestCase
from ..testing.utils import disable_warnings, get_random_string


class DevicepatternsViewTestCase(PluginViewTestCase):
    """Test Devicepatterns views."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Devicepatterns.objects.create(name='View Test 1')
        Devicepatterns.objects.create(name='View Test 2')
        Devicepatterns.objects.create(name='View Test 3')

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.base_url = 'plugins:netbox_device_patterns_plugin:devicepatterns'

    def test_list_devicepatternss(self):
        """Test Devicepatterns list view."""
        self.add_permissions('netbox_device_patterns_plugin.view_devicepatterns')

        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_devicepatternss_without_permission(self):
        """Test Devicepatterns list view without permission."""
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_devicepatterns(self):
        """Test Devicepatterns detail view."""
        self.add_permissions('netbox_device_patterns_plugin.view_devicepatterns')

        instance = Devicepatterns.objects.first()
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_devicepatterns(self):
        """Test creating a Devicepatterns via form."""
        self.add_permissions(
            'netbox_device_patterns_plugin.add_devicepatterns',
            'netbox_device_patterns_plugin.view_devicepatterns'
        )

        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_add')
        name = f'Created {get_random_string(10)}'

        form_data = self.post_data({
            'name': name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was created
        instance = Devicepatterns.objects.get(name=name)
        self.assertEqual(instance.name, name)

    def test_create_devicepatterns_without_permission(self):
        """Test creating a Devicepatterns without permission."""
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_devicepatterns(self):
        """Test editing a Devicepatterns via form."""
        self.add_permissions(
            'netbox_device_patterns_plugin.change_devicepatterns',
            'netbox_device_patterns_plugin.view_devicepatterns'
        )

        instance = Devicepatterns.objects.first()
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_edit', kwargs={'pk': instance.pk})

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data({
            'name': new_name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was updated
        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_delete_devicepatterns(self):
        """Test deleting a Devicepatterns."""
        self.add_permissions(
            'netbox_device_patterns_plugin.delete_devicepatterns',
            'netbox_device_patterns_plugin.view_devicepatterns'
        )

        instance = Devicepatterns.objects.first()
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_delete', kwargs={'pk': instance.pk})

        # Confirm deletion
        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was deleted
        self.assertFalse(
            Devicepatterns.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_devicepatterns_without_permission(self):
        """Test deleting a Devicepatterns without permission."""
        instance = Devicepatterns.objects.first()
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class DevicepatternsFormTestCase(PluginViewTestCase):
    """Test Devicepatterns form validation."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions(
            'netbox_device_patterns_plugin.add_devicepatterns',
            'netbox_device_patterns_plugin.view_devicepatterns'
        )

    def test_form_validation_empty_name(self):
        """Test form validation with empty name."""
        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_add')
        form_data = self.post_data({'name': ''})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should not create object
        self.assertEqual(Devicepatterns.objects.filter(name='').count(), 0)

    def test_form_validation_duplicate_name(self):
        """Test form validation with duplicate name."""
        Devicepatterns.objects.create(name='Duplicate')

        url = reverse('plugins:netbox_device_patterns_plugin:devicepatterns_add')
        form_data = self.post_data({'name': 'Duplicate'})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should only have one instance with this name
        self.assertEqual(Devicepatterns.objects.filter(name='Duplicate').count(), 1)
