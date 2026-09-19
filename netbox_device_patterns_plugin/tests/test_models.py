"""
Test cases for NetBox Device Patterns Plugin models.
"""

from django.core.exceptions import ValidationError

from ..models import Devicepatterns
from ..testing import PluginModelTestCase
from ..testing.utils import create_tags, get_random_string


class DevicepatternsTestCase(PluginModelTestCase):
    """Test Devicepatterns model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        # Create test instances
        Devicepatterns.objects.create(name='Test 1')
        Devicepatterns.objects.create(name='Test 2')
        Devicepatterns.objects.create(name='Test 3')

    def test_create_devicepatterns(self):
        """Test creating a Devicepatterns instance."""
        name = f'Test {get_random_string(10)}'
        instance = Devicepatterns.objects.create(name=name)

        self.assertEqual(instance.name, name)
        self.assertIsNotNone(instance.pk)

    def test_devicepatterns_str(self):
        """Test Devicepatterns string representation."""
        instance = Devicepatterns.objects.first()
        self.assertEqual(str(instance), instance.name)

    def test_devicepatterns_absolute_url(self):
        """Test Devicepatterns get_absolute_url method."""
        instance = Devicepatterns.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_devicepatterns_unique_name(self):
        """Test that Devicepatterns names must be unique."""
        name = 'Duplicate Name'
        Devicepatterns.objects.create(name=name)

        with self.assertRaises(ValidationError):
            instance = Devicepatterns(name=name)
            instance.full_clean()

    def test_model_to_dict(self):
        """Test model_to_dict helper method."""
        instance = Devicepatterns.objects.first()
        data = self.model_to_dict(instance)

        self.assertIn('name', data)
        self.assertEqual(data['name'], instance.name)
        self.assertIn('id', data)

    def test_instance_equal(self):
        """Test assertInstanceEqual helper method."""
        instance = Devicepatterns.objects.first()

        # Should pass with matching data
        self.assertInstanceEqual(
            instance,
            {'name': instance.name, 'id': instance.pk}
        )

    def test_devicepatterns_with_tags(self):
        """Test Devicepatterns with tags."""
        tags = create_tags(['important', 'test'])
        instance = Devicepatterns.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_bulk_create(self):
        """Test bulk creation of Devicepatterns instances."""
        initial_count = Devicepatterns.objects.count()

        instances = [
            Devicepatterns(name=f'Bulk {i}')
            for i in range(5)
        ]
        Devicepatterns.objects.bulk_create(instances)

        self.assertEqual(
            Devicepatterns.objects.count(),
            initial_count + 5
        )

    def test_query_filter(self):
        """Test filtering Devicepatterns instances."""
        # Create a specific instance for filtering
        test_name = f'FilterTest {get_random_string(10)}'
        Devicepatterns.objects.create(name=test_name)

        # Test filter
        results = Devicepatterns.objects.filter(name=test_name)
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, test_name)

    def test_ordering(self):
        """Test Devicepatterns default ordering."""
        instances = list(Devicepatterns.objects.all())

        # Check that instances are ordered by name
        names = [instance.name for instance in instances]
        self.assertEqual(names, sorted(names))


class DevicepatternsValidationTestCase(PluginModelTestCase):
    """Test Devicepatterns validation."""

    def test_empty_name(self):
        """Test that empty name is not allowed."""
        with self.assertRaises(ValidationError):
            instance = Devicepatterns(name='')
            instance.full_clean()

    def test_name_max_length(self):
        """Test name field max length."""
        long_name = 'x' * 101  # Exceeds max_length of 100

        with self.assertRaises(ValidationError):
            instance = Devicepatterns(name=long_name)
            instance.full_clean()
