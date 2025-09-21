#A PriceLevel is just a queue of Order objects all with the same price.
from lob.order import Order
from collections import deque
from typing import Optional, Iterator


class PriceLevel:

    def __init__(self, symbol:str ,price:float):
        self.symbol= symbol
        self.price = price
        self.queue = deque() # double ended queue with the orders
        
    def append(self,order:Order) -> None:
        """Append a new resting order to the tail (time priority)."""
        if (self.symbol == order.symbol)&(order.price == self.price):
            self.queue.append(order)
        else: raise ValueError(f"Order price {order.price} != level price {self.price} or differt Symble ")

    # Take the first order in     
    def peek(self) -> None:
        """Return the first order without removing it."""
        if not self.queue:
            return None 
        else:
            return self.queue[0]

    
    def popleft(self):
        """Remove and return the first order (or None if empty)."""
        if self.queue:
            return self.queue.popleft()
        else: None

    def cancel(self, order_id: int) -> bool:
        """
        Remove the order with this id if present; return True if removed, else False.
        """
        for i, o in enumerate(self.queue):
            if o.orderid == order_id:
                del self.queue[i]      # preserves relative order of the rest
                return True
        return False
    
    def total_qty(self) -> int:
        """Sum remaining quantity of all active orders at this price."""
        return sum(o.qty for o in self.queue if o.qty > 0)

    def __len__(self) -> int:
        "Return the lenght of the queue"
        return len(self.queue)

    def __iter__(self) -> Iterator[Order]:
        return iter(self.queue)