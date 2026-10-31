import pytest

from weconomy.graph import event_edge_query


def test_relationship_type_not_interpolated_from_untrusted_input():
    assert "edge:ACQUIRED" in event_edge_query("ACQUIRED")
    with pytest.raises(ValueError):
        event_edge_query("ACQUIRED] DELETE n //")
