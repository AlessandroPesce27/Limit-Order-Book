from lob.types import Side, OrderId, Price, Qty, Timestamp,Symbol,Exchange 

class Order:
    
    def __init__(self, 
                 symbol:Symbol ,
                 exchange:Exchange,
                 orderid:OrderId ,
                 side:Side ,
                 price:Price,
                 qty:Qty,
                 timestamp:Timestamp
                 ):
        
        self.side = side
        self.symbol = symbol
        self.exchange = exchange
        self.orderid = orderid
        self.price = price
        self.qty = qty
        self.timestamp = timestamp
        
        # As a first thing we validate data before so we catch the mistake early
        if self.side not in  {"B", "S"}:
            raise ValueError(f'invalid {self.side} must be B or S') 
        
        if not isinstance(self.exchange, Exchange):
            raise ValueError(f'invalid {self.exchange}, must be of type Str')
        
        if not isinstance(self.symbol,Symbol):
            raise ValueError(f'invalid {self.symbol}, must be of type Str')

        if self.price <= 0:
            raise ValueError(f'invalid {self.price} must be positive')  
        
        if self.qty <=0: 
            raise ValueError(f'invalid {self.qty} must be >0') 

        if self.timestamp < 0:
            raise ValueError(f'invalid {self.timestamp} must be >= 0') 
        
        if self.orderid <=0:
            raise ValueError(f'invalid {self.orderid} must be >= 0') 
        
    #this return the info to the book wether the order is active or not 
    @property
    def is_active(self) ->  bool :
        "An order is active when qty > 0, when qty = 0 order is filled or canceld"
        if self.qty > 0:
            return True


    #this Mutate the quantity
    def reduce(self, q:int) -> None:
        "quantity q is how much of the order has been filled. "
        "if q < 0 -> we return ValueError"
        "if q>qty -> we send the qty to 0 "
        
        if q < 0 : 
            raise ValueError("quantity cannot be negative")
        elif q > self.qty :
            self.qty = 0
        else: self.qty = self.qty - q




