from lob.price_level import PriceLevel
from lob.order import Order
import pytest
from datetime import datetime

def test_price_level_basic_fifo():
    """Tests that orders are added and removed in First-In-First-Out order."""
    pl = PriceLevel(symbol="TEST", price=10000)
    
    # Create Order objects with all required arguments
    o1 = Order(symbol="TEST", exchange="XTEST", orderid=1, side="B", price=10000, qty=5, timestamp=datetime.now())
    o2 = Order(symbol="TEST", exchange="XTEST", orderid=2, side="B", price=10000, qty=3, timestamp=datetime.now())

    pl.append(o1)
    pl.append(o2)

    # FIFO: The first order in (o1) should be the head of the queue
    head = pl.peek()
    assert head.orderid == 1
    assert len(pl) == 2

    # Total quantity should be the sum of the order quantities
    assert pl.total_qty() == 8

    # Removing the head should reveal the next order (o2)
    popped = pl.popleft()
    assert popped.orderid == 1
    assert pl.peek().orderid == 2
    assert len(pl) == 1
    assert pl.total_qty() == 3

def test_price_level_cancel_and_not_found():
    """Tests that a specific order can be cancelled from the queue."""
    pl = PriceLevel(symbol="TEST", price=10000)
    
    o1 = Order(symbol="TEST", exchange="XTEST", orderid=10, side="S", price=10000, qty=2, timestamp=datetime.now())
    o2 = Order(symbol="TEST", exchange="XTEST", orderid=11, side="S", price=10000, qty=2, timestamp=datetime.now())
    pl.append(o1)
    pl.append(o2)

    # Cancel an existing order
    assert pl.cancel(10) is True
    assert len(pl) == 1
    assert pl.peek().orderid == 11
    assert pl.total_qty() == 2

    # Attempt to cancel a non-existent order
    assert pl.cancel(999) is False
    assert len(pl) == 1  # Unchanged

def test_price_mismatch_rejected():
    """Tests that an order with the wrong price is rejected."""
    pl = PriceLevel(symbol="TEST", price=10000)
    
    # This order has a price of 9950, which does not match the level's price of 10000
    bad_order = Order(symbol="TEST", exchange="XTEST", orderid=3, side="B", price=9950, qty=1, timestamp=datetime.now())
    
    # The PriceLevel should raise a ValueError
    with pytest.raises(ValueError):
        pl.append(bad_order)