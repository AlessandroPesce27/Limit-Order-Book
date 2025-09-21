import pytest
from lob.order import Order

def test_order_valid():
    o = Order(1, "B", 100.0, 5, 0)
    assert o.is_active
    assert o.qty == 5

def test_reduce_to_zero():
    o = Order(2, "S", 101.0, 3, 1)
    o.reduce(2)
    assert o.qty == 1
    o.reduce(10)
    assert o.qty == 0
    assert not o.is_active

def test_invalid_inputs():
    with pytest.raises(ValueError): Order(3, "X", 100.0, 1, 0)
    with pytest.raises(ValueError): Order(4, "B", -1.0, 1, 0)
    with pytest.raises(ValueError): Order(5, "S", 100.0, 0, 0)
    with pytest.raises(ValueError): Order(6, "B", 100.0, 1, -1)
    with pytest.raises(ValueError): Order(0, "B", 100.0, 1, 0)

def test_reduce_negative_amount():
    o = Order(7, "B", 100.0, 2, 0)
    with pytest.raises(ValueError):
        o.reduce(-1)