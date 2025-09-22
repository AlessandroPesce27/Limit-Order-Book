# tests/test_matching_engine.py
import pytest
from datetime import datetime
from lob.order_book import OrderBook, Trade
from lob.order import Order

@pytest.fixture
def empty_book():
    """Returns a new, empty OrderBook for a sample symbol."""
    return OrderBook(symbol="TEST", exchange="XTEST")

def test_simple_full_match(empty_book):
    """
    Tests a simple full match between one resting ask and one aggressive bid.
    """
    # Arrange
    book = empty_book
    
    # A passive sell order for 10 shares at $100
    passive_sell_order = Order(
        symbol="TEST",
        exchange="XTEST",
        orderid=1,
        side='S',
        price=10000,
        qty=10,
        timestamp=datetime.now() # <-- Added missing arguments
    )
    book.add_order(passive_sell_order)
    
    # An aggressive buy order that should match the sell order
    aggressive_buy_order = Order(
        symbol="TEST",
        exchange="XTEST",
        orderid=2,
        side='B',
        price=10000,
        qty=10,
        timestamp=datetime.now() # <-- Added missing arguments
    )

    # Act
    trades = book.process_order(aggressive_buy_order)

    # Assert
    assert len(trades) == 1
    trade = trades[0]
    
    assert isinstance(trade, Trade)
    assert trade.qty == 10
    assert trade.price == 10000
    assert trade.maker_order_id == 1
    assert trade.taker_order_id == 2
    
    assert book.best_bid() is None
    assert book.best_ask() is None
    assert len(book.index) == 0