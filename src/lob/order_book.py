# Here we create the OrderBook
from lob.price_level import PriceLevel
from lob.order import Order
from typing import Dict,Tuple

class OrderBook:
    
    def __init__ (self, symbol, exchange):
        self.exchange = exchange
        self.symbol = symbol
        self.bids = {} # maps dict of price --> bid pricelevel queue. initialized as empty at the beg of the day
        self.asks = {} # maps dict of price --> ask pricelevel queue.initialized as empty at the beg of the day
        self.index = {} # map of the order_id --> (side,price).to help us find order soon 

    def add_order(self,order:Order):
        
        if order.side == 'B':
            if order.price in self.bids: 
                 self.bids[order.price].append(order)
            else:
                self.bids[order.price] = PriceLevel(order.symbol,order.price)
                self.bids[order.price].append(order)


        if order.side == 'S':
            if order.price in self.asks: 
                self.asks[order.price].append(order)
            else:
                self.asks[order.price] = PriceLevel(order.symbol,order.price)
                self.asks[order.price].append(order)

        self.index[order.orderid] = (order.side,order.price)

    def best_bid(self):
        return(max(self.bids.keys(),None))
    
    def best_ask(self):
        return(min(self.asks.keys(),None))
    
    def cancel_order(self, order:Order):

        if order.orderid not in self.index:
            return False
        else: 
            side = self.index[order.orderid][0]
            price = self.index[order.orderid][1]
            
            if side =='B':

                if self.bids[price].cancel(order.orderid) == True: # removing using method from PriceLevel and checking all in the same line 
                    del self.index[order.orderid] # we remove it also from the index list 

            else:  
                if self.asks[price].cancel(order.orderid) == True:
                    del self.index[order.orderid]   

    def process_order(self,order:Order):
        ## COntinue from Here!!!