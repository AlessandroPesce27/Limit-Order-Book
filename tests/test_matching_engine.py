import pytest
from datetime import datetime
from lob.order_book import OrderBook, Trade
from lob.order import Order

# This fixture creates a fresh, empty OrderBook for each test function.
@pytest.fixture
def book():
    """Returns a new, empty OrderBook for a sample symbol."""
    return OrderBook(symbol="TEST", exchange="XTEST")

def test_add_passive_order_no_trades(book):
    """Tests that a simple passive order is added correctly without generating trades."""
    # Arrange
    order = Order("TEST", "XTEST", 1, 'B', 9900, 10, datetime.now())

    # Act
    trades = book.process_order(order)

    # Assert
    assert len(trades) == 0
    assert book.best_bid() == 9900
    assert len(book.index) == 1

def test_simple_full_match_buy_side(book):
    """Tests a simple full match: one resting ask, one aggressive bid."""
    # Arrange
    book.add_order(Order("TEST", "XTEST", 1, 'S', 10000, 10, datetime.now()))
    aggressive_buy = Order("TEST", "XTEST", 2, 'B', 10000, 10, datetime.now())

    # Act
    trades = book.process_order(aggressive_buy)

    # Assert
    assert len(trades) == 1
    trade = trades[0]
    assert trade.qty == 10
    assert trade.price == 10000
    assert trade.maker_order_id == 1
    assert trade.taker_order_id == 2
    assert book.best_ask() is None and book.best_bid() is None
    assert len(book.index) == 0

def test_simple_full_match_sell_side(book):
    """Tests a simple full match: one resting bid, one aggressive ask."""
    # Arrange
    book.add_order(Order("TEST", "XTEST", 1, 'B', 10000, 10, datetime.now()))
    aggressive_sell = Order("TEST", "XTEST", 2, 'S', 10000, 10, datetime.now())

    # Act
    trades = book.process_order(aggressive_sell)

    # Assert
    assert len(trades) == 1
    trade = trades[0]
    assert trade.qty == 10
    assert trade.price == 10000
    assert trade.maker_order_id == 1
    assert trade.taker_order_id == 2
    assert book.best_ask() is None and book.best_bid() is None
    assert len(book.index) == 0

def test_partial_fill_resting_order_is_larger(book):
    """Tests a partial fill where the aggressive order is smaller."""
    # Arrange
    book.add_order(Order("TEST", "XTEST", 1, 'S', 10000, 50, datetime.now()))
    aggressive_buy = Order("TEST", "XTEST", 2, 'B', 10000, 10, datetime.now())

    # Act
    trades = book.process_order(aggressive_buy)

    # Assert
    assert len(trades) == 1
    assert trades[0].qty == 10
    assert book.best_ask() == 10000
    # The resting order should still be on the book with reduced quantity
    resting_order = book.asks[10000].peek()
    assert resting_order.orderid == 1
    assert resting_order.qty == 40
    assert len(book.index) == 1

def test_partial_fill_taker_order_is_larger(book):
    """Tests a partial fill where the aggressive order is larger and becomes a new resting order."""
    # Arrange
    book.add_order(Order("TEST", "XTEST", 1, 'S', 10000, 10, datetime.now()))
    aggressive_buy = Order("TEST", "XTEST", 2, 'B', 10000, 50, datetime.now())

    # Act
    trades = book.process_order(aggressive_buy)

    # Assert
    assert len(trades) == 1
    assert trades[0].qty == 10
    assert book.best_ask() is None # The ask side should be cleared
    # The remainder of the aggressive order should now be the best bid
    assert book.best_bid() == 10000
    new_resting_order = book.bids[10000].peek()
    assert new_resting_order.orderid == 2
    assert new_resting_order.qty == 40
    assert len(book.index) == 1

def test_multi_level_fill(book):
    """Tests an aggressive order that clears multiple price levels."""
    # Arrange
    book.add_order(Order("TEST", "XTEST", 1, 'S', 10000, 10, datetime.now()))
    book.add_order(Order("TEST", "XTEST", 2, 'S', 10001, 15, datetime.now()))
    aggressive_buy = Order("TEST", "XTEST", 3, 'B', 10001, 30, datetime.now())

    # Act
    trades = book.process_order(aggressive_buy)

    # Assert
    assert len(trades) == 2
    # First trade at the best price
    assert trades[0].price == 10000 and trades[0].qty == 10
    # Second trade at the next best price
    assert trades[1].price == 10001 and trades[1].qty == 15
    
    assert book.best_ask() is None # Ask side is cleared
    # Remainder of the aggressive order becomes the new best bid
    assert book.best_bid() == 10001
    assert book.bids[10001].peek().qty == 5 # 30 - 10 - 15 = 5
    assert len(book.index) == 1