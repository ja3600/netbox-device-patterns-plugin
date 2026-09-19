from typing import Dict, Any, List
from .models import Project, EndpointInstance, PhysicalLink


def build_project_graph(project: Project) -> Dict[str, Any]:
    """
    Build a JSON graph for the project:
    - Nodes: endpoints + devices
    - Edges: PhysicalLink records
    - Port tags: endpoint_interface_name + device_interface.name

    Return structure:
    {
      "nodes": [
        {"id": "ep:12", "type": "endpoint", "label": "RTU-1", "definition": "SEL-3530", ...},
        {"id": "dev:34", "type": "device", "label": "SEL-3505", ...},
        ...
      ],
      "edges": [
        {
          "id": "link:56",
          "source": "ep:12",
          "target": "dev:34",
          "endpoint_port_tag": "eth0",
          "device_port_tag": "Gi1/0/3",
        },
        ...
      ]
    }
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    # --- Nodes: endpoints ---
    endpoint_nodes = {}
    for ep in project.endpoints.select_related('definition', 'device'):
        node_id = f'ep:{ep.pk}'
        endpoint_nodes[ep.pk] = node_id

        nodes.append({
            "id": node_id,
            "type": "endpoint",
            "label": ep.name,
            "definition": ep.definition.name,
            "role": ep.definition.role,
            "category": ep.definition.category,
            "device": ep.device.name if ep.device else None,
        })

    # --- Nodes: devices ---
    device_nodes = {}
    # Collect devices from links + endpoint.device
    devices = set()

    # Devices from endpoint.device
    for ep in project.endpoints.select_related('device'):
        if ep.device:
            devices.add(ep.device)

    # Devices from PhysicalLink
    links_qs = PhysicalLink.objects.filter(endpoint__project=project).select_related('device', 'device_interface', 'endpoint')
    for link in links_qs:
        if link.device:
            devices.add(link.device)

    for dev in devices:
        node_id = f'dev:{dev.pk}'
        device_nodes[dev.pk] = node_id

        nodes.append({
            "id": node_id,
            "type": "device",
            "label": dev.name,
            "device_type": getattr(dev.device_type, "model", None),
            "role": getattr(dev, "role", None),
        })

    # --- Edges: physical links ---
    for link in links_qs:
        ep = link.endpoint
        dev = link.device

        source_id = endpoint_nodes.get(ep.pk)
        target_id = device_nodes.get(dev.pk)

        if not source_id or not target_id:
            continue  # safety

        edges.append({
            "id": f'link:{link.pk}',
            "source": source_id,
            "target": target_id,
            "endpoint_port_tag": link.endpoint_interface_name,
            "device_port_tag": link.device_interface.name if link.device_interface else None,
        })

    graph = {
        "project": {
            "id": project.pk,
            "name": project.name,
            "site": project.site.name if project.site else None,
        },
        "nodes": nodes,
        "edges": edges,
    }

    return graph
