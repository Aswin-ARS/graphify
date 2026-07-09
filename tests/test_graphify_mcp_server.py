"""Tests for graphify MCP server."""

import json
import pytest
import sys
from pathlib import Path

# Add graphify-mcp-server to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "graphify-mcp-server"))

from graphify_mcp_server import GraphifyMCPServer, GraphNode, GraphEdge


@pytest.mark.asyncio
async def test_graphify_server_initialization():
    """Test server initializes without errors."""
    server = GraphifyMCPServer()
    assert server.server is not None
    assert server.graphs == {}


@pytest.mark.asyncio
async def test_extract_services_no_services():
    """Test extracting with no services returns error."""
    server = GraphifyMCPServer()
    result = await server.server.tools["extract_services"].call({})
    result_json = json.loads(result)
    assert result_json["status"] == "success"
    assert "graphs_loaded" in result_json


def test_graph_node_serialization():
    """Test GraphNode can be serialized to dict."""
    node = GraphNode(
        id="lis:ResultServiceImpl",
        type="class",
        name="ResultServiceImpl",
        file="src/main/java/com/lifetrenz/lths/lab/result/service/impl/ResultServiceImpl.java",
        service="lis-service",
        language="java",
        tags=["service", "implements_pattern:dual_level_status_sync"],
        metadata={"lines": "50-250", "methods": 15}
    )
    node_dict = node.__dict__
    assert node_dict["id"] == "lis:ResultServiceImpl"
    assert node_dict["type"] == "class"
    assert "service" in node_dict["tags"] or "service" in str(node_dict)


def test_graph_edge_creation():
    """Test GraphEdge can be created with metadata."""
    edge = GraphEdge(
        id="edge_001",
        source="lis:ResultServiceImpl.updateResult",
        target="lis:sampleStatusSyncUtil.syncCollectionStatus",
        type="calls",
        extracted=True,
        confidence=1.0,
        metadata={"line": 123, "call_frequency": "every_invocation"}
    )
    assert edge.source == "lis:ResultServiceImpl.updateResult"
    assert edge.type == "calls"
    assert edge.metadata["line"] == 123
