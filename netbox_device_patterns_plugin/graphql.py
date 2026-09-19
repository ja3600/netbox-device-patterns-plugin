"""
GraphQL schema for NetBox Device Patterns Plugin.

For more information on NetBox GraphQL, see:
https://docs.netbox.dev/en/stable/plugins/development/graphql/

For Strawberry GraphQL documentation, see:
https://strawberry.rocks/
"""


import strawberry
import strawberry_django

from .models import Devicepatterns


@strawberry_django.type(
    Devicepatterns,
    fields='__all__',
)
class DevicepatternsType:
    """GraphQL type for Devicepatterns model."""
    pass


@strawberry.type(name="Query")
class DevicepatternsQuery:
    """GraphQL queries for NetBox Device Patterns Plugin."""

    devicepatterns: DevicepatternsType = strawberry_django.field()
    devicepatterns_list: list[DevicepatternsType] = strawberry_django.field()


schema = [
    DevicepatternsQuery,
]

