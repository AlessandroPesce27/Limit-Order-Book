# Here we create the OrderBook
from lob.price_level import PriceLevel
from lob.order import Order
from typing import Dict,Tuple
from dataclasses import dataclass 

# dataclasses are basically classes but with alreary integrated some dunder methods 
# usefull when class have just co collect data 
@dataclass 
class Trade:
    qty: int
    price: int
    maker_order_id: int # The MAKER --> is the passive order 'making the market'
    take_order_id: int ## The TAKER --> is the aggressive order 'taking the market'


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



    def process_order(self, order: Order):
        trades = []

        if order.side == 'B':
            #Aggressive BUY order
            if self.best_ask() is not None and order.price >= self.best_ask():
                trades = self.matching_engine(order)
            else:
                # It's a passive buy order
                self.add_order(order)
    
    ## CONTINUE WITH THE OTHER SIDE OF THE PROCESSING (should be the same logic inverted in signs)

    
    def matching_engine(self, incoming_order:Order):
        "we trade --> we take best bid with the best asks "
        "we look for the qty in price level orders we clear the cleareble qty "
        "then we reduce the orders and update the Pricelevels queues accordingly" 
        trades=[]
        
        while (incoming_order.qty>0) and (incoming_order.price>=self.best_ask()) and (self.best_ask() is not None):
            best_price = self.best_ask()
            best_price_level_queue = self.asks[best_price] # bestprice queue
            best_matching_order = best_price_level_queue.peek() # this return the firstm order(head) of the queue of that price level 
            
            #Trade 
            traded_quantity = min(best_matching_order.qty,incoming_order.qty)

            trade = Trade(qty=traded_quantity, 
                          price=best_price, 
                          maker_order_id = best_matching_order.orderid,
                          take_order_id = incoming_order.orderid 
                          )            
            
            #reduce the quantity of the orders by the cleared volumes
            # recall that that reduce() sends to 0 qty if q>qty
            incoming_order.reduce(traded_quantity) #reduce bid
            best_matching_order.reduce(traded_quantity) #reduce ask

            
            if best_matching_order.qty == 0:
        
                cleared_ask_order = best_price_level_queue.popleft() #remove from the pricelevelqueue the cleared order
                del self.index[cleared_ask_order.orderid] #and remove if from the dictionary

                # if the entire price level is empty --> remove the pricelevel queue
                if len(best_price_level_queue)==0:
                    del self.asks[best_price] # remove the entire empty queue to the while check the next best_ask in the OB automatically

            trades.append(trade)

        # If the incoming order is not cleared completely we add it in the resting order 
        if incoming_order.qty>0:
            self.add_order(incoming_order)

        return trades



            

