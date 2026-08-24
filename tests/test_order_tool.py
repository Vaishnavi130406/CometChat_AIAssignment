from app.order_tool import OrderTool


def test_valid_order_lookup():
    tool = OrderTool()

    result = tool.get_order("ORD-1007")

    assert result is not None
    assert result["order_id"] == "ORD-1007"
    assert result["status"] == "shipped"


def test_lowercase_and_whitespace_are_normalized():
    tool = OrderTool()

    result = tool.get_order("  ord-1007  ")

    assert result is not None
    assert result["order_id"] == "ORD-1007"


def test_unknown_order_returns_none():
    tool = OrderTool()

    result = tool.get_order("ORD-9999")

    assert result is None


def test_invalid_order_id_does_not_guess():
    tool = OrderTool()

    result = tool.get_order("ORD-100")

    assert result is None


def test_private_customer_data_is_not_exposed():
    tool = OrderTool()

    result = tool.get_order("ORD-1007")

    assert result is not None

    assert "customer" not in result
    assert "name" not in result
    assert "email" not in result
    assert "shipping_address" not in result


def test_internal_data_is_not_exposed():
    tool = OrderTool()

    result = tool.get_order("ORD-1005")

    assert result is not None

    assert "internal" not in result
    assert "risk_score" not in result
    assert "warehouse_note" not in result
    assert "support_tags" not in result


def test_cancelled_order_keeps_authoritative_status():
    tool = OrderTool()

    result = tool.get_order("ORD-1004")

    assert result is not None
    assert result["status"] == "cancelled"


def test_shipped_order_without_eta_does_not_invent_eta():
    tool = OrderTool()

    result = tool.get_order("ORD-1011")

    assert result is not None
    assert result["status"] == "shipped"
    assert result["estimated_delivery"] is None