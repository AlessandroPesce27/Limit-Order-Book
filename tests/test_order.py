import pytest
from lob.order import Order
from datetime import datetime

def test_order_valid():
    """Tests that a valid Order object can be created and is active."""
    o = Order(
        symbol="TEST", 
        exchange="XTEST", 
        orderid=1, 
        side="B", 
        price=10000, 
        qty=5, 
        timestamp=datetime.now()
    )
    assert o.is_active
    assert o.qty == 5

def test_reduce_quantity():
    """Tests that the reduce method correctly adjusts the order's quantity."""
    o = Order(
        symbol="TEST", 
        exchange="XTEST", 
        orderid=2, 
        side="S", 
        price=10100, 
        qty=10, 
        timestamp=datetime.now()
    )
    # Reduce by a smaller amount
    o.reduce(3)
    assert o.qty == 7
    assert o.is_active

    # Reduce by a larger amount (should set qty to 0)
    o.reduce(10)
    assert o.qty == 0
    assert not o.is_active

def test_invalid_inputs():
    """Tests that the Order class raises ValueErrors for invalid constructor arguments."""
    now = datetime.now()
    # Invalid side
    with pytest.raises(ValueError): Order("TEST", "XTEST", 3, "X", 10000, 1, now)
    # Invalid price
    with pytest.raises(ValueError): Order("TEST", "XTEST", 4, "B", -100, 1, now)
    # Invalid quantity
    with pytest.raises(ValueError): Order("TEST", "XTEST", 5, "S", 10000, 0, now)
    # Invalid order ID
    with pytest.raises(ValueError): Order("TEST", "XTEST", 0, "B", 10000, 1, now)


def test_reduce_negative_amount():
    """Tests that reducing by a negative quantity raises a ValueError."""
    o = Order(
        symbol="TEST", 
        exchange="XTEST", 
        orderid=7, 
        side="B", 
        price=10000, 
        qty=2, 
        timestamp=datetime.now()
    )
    with pytest.raises(ValueError):
        o.reduce(-1)
