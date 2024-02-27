from enum import Enum

class OrderType(str, Enum):
    LIMIT_ORDER = "limit_order"
    MARKET_ORDER = "market_order"
