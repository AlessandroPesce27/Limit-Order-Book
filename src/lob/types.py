#in this file we create the "Vocabulary for the LOB" 

from typing import Literal 

Side = Literal['B','S'] # buy ore sell
Symbol = str
Exchange = str
OrderId = int
Price = int # in cents
Qty = int
Timestamp = int