from lob.price_level import PriceLevel
from lob.order import Order
import pytest

def test_price_level_basic_fifo():
    pl = PriceLevel(100.0)
    o1 = Order(1, "B", 100.0, 5, 0)
    o2 = Order(2, "B", 100.0, 3, 1)

    pl.append(o1)
    pl.append(o2)

    # FIFO
    head = pl.peek()
    assert head.order_id == 1
    assert len(pl) == 2

    # total qty is sum
    assert pl.total_qty() == 8

    # removing head changes peek
    popped = pl.popleft()
    assert popped.order_id == 1
    assert pl.peek().order_id == 2
    assert len(pl) == 1
    assert pl.total_qty() == 3

def test_price_level_cancel_and_not_found():
    pl = PriceLevel(100.0)
    o1 = Order(10, "S", 100.0, 2, 0)
    o2 = Order(11, "S", 100.0, 2, 1)
    pl.append(o1)
    pl.append(o2)

    assert pl.cancel(10) is True  # removed head
    assert len(pl) == 1
    assert pl.peek().order_id == 11
    assert pl.total_qty() == 2

    # cancel non-existent id
    assert pl.cancel(999) is False
    assert len(pl) == 1  # unchanged

def test_price_mismatch_rejected():
    pl = PriceLevel(100.0)
    bad = Order(3, "B", 99.5, 1, 0)
    with pytest.raises(ValueError):
        pl.append(bad)