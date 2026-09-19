"""
Test cases for NetBox Device Patterns Plugin GraphQL API.
"""
from ..models import Devicepatterns
from ..testing import PluginGraphQLTestCase


class DevicepatternsGraphQLTestCase(PluginGraphQLTestCase):
    """Test Devicepatterns GraphQL queries."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Devicepatterns.objects.create(name='GraphQL Test 1')
        Devicepatterns.objects.create(name='GraphQL Test 2')
        Devicepatterns.objects.create(name='GraphQL Test 3')

    def test_query_devicepatterns(self):
        """Test GraphQL query for a single Devicepatterns."""
        self.add_permissions('netbox_device_patterns_plugin.view_devicepatterns')

        instance = Devicepatterns.objects.first()

        query = (
            "query { "
            "devicepatterns(id: " + str(instance.pk) + ") { "
            "id name "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['devicepatterns']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)

    def test_query_devicepatterns_list(self):
        """Test GraphQL query for list of Devicepatternss."""
        self.add_permissions('netbox_device_patterns_plugin.view_devicepatterns')

        query = """
        query {
            devicepatterns_list {
                id
                name
            }
        }
        """

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['devicepatterns_list']
        self.assertEqual(len(data), 3)
        self.assertIn('id', data[0])
        self.assertIn('name', data[0])

    def test_query_devicepatterns_with_all_fields(self):
        """Test GraphQL query with all available fields."""
        self.add_permissions('netbox_device_patterns_plugin.view_devicepatterns')

        instance = Devicepatterns.objects.first()

        query = (
            "query { "
            "devicepatterns(id: " + str(instance.pk) + ") { "
            "id name created last_updated "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['devicepatterns']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)
        self.assertIsNotNone(data['created'])
        self.assertIsNotNone(data['last_updated'])

