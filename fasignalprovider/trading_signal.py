from pydantic import BaseModel, Field, field_validator

# from typing import Optional
from datetime import datetime
from fasignalprovider.direction import Direction
from fasignalprovider.order_type import OrderType
from fasignalprovider.side import Side


class TradingSignal(BaseModel):
    """
    A trading signal represents a suggestion to buy or sell. It is issued by a signal supplier
    (manually or algorithmically). It must have a correlating id to a trade.
    """

    provider_signal_id: str = Field(
        ...,
        description="Mandatory. Provide us with your signal id. This correlation id is your own 'signal id' \
            of your internal system. Your and our party will use it to inspect process errors. \
            Do NOT mistaken this correlation id with the trade id.",
    )

    provider_trade_id: str = Field(
        ...,
        description="Mandatory. We describes a trade as a buy and a sell (not soley a buy OR a sell), \
            which has a unique provider_trade_id (the same for both, respectively all of them). \
            Every trade is expected to consist of at least one buy signal and at least one sell signal.\
            Both have a unique provider_signal_id, but - again - share the same provider_trade_id. \
            Thus, the provider_trade_id is mandatory for each signal sent. This will allow to create \
            a multi-position-trade. \
            \
            E.g. one can send one long signal with a provider_trade_id 77 and another long signal a \
            few hours later also with the provider_trade_id 77. Still, both signals require their \
            unique provider_signal_id. Provided that the position_size_in_percentage is less than \
            100 on the first one. \
            All updates provided by Freya Alpha will hold the provider_trade_id and likely the provider_signal_id \
            - if it concerns a signal itself.",
    )

    provider_id: str = Field(
        ..., description="Mandatory. Your ID as a provider, who emitted the signal."
    )
    strategy_id: str = Field(
        ...,
        description="Mandatory. Provide the id of the strategy (you might have more than one algorithm), which is sending a signal.",
    )

    is_hot_signal: bool = Field(
        default=False,
        description="Mandatory. By DEFAULT, every signal is marked as a COLD SIGNAL.  \
            That is a paper-trading signal and will only be processed for forward-performance \
            testing. Hot signals are suggested to be processed by the order engines - \
            provided all other requirements for hot trading are fulfilled. Set this \
            value to true to suggest a hot trade.",
    )
    market: str = Field(
        ..., description="Mandatory. The market you want to trade. e.g. BTC/USDT"
    )
    data_source: str = Field(
        ...,
        description="Mandatory. The source of data you based your decision on. E.g. Binance, CoinMarketCap,\
            Chainlink, etc. This is to safeguard investments, which base on manipulated data sources.",
    )
    direction: Direction = Field(..., description="Mandatory. Simply LONG or SHORT.")
    side: Side = Field(
        ..., description="Mandatory. Simply BUY (open trade) or SELL (close trade)."
    )
    order_type: OrderType = Field(
        default=OrderType.LIMIT_ORDER,
        description="Mandatory. Default is Limit Order. Please be careful with Markets Orders as slipage could be high.",
    )
    price: float = Field(
        ...,
        description="Mandatory. The price to buy or sell. Used for the limit-order. If market-order is set, this price is a reference price only to avoid average slipage greater than 10%.",
    )
    tp: float = Field(
        ...,
        description="Mandatory. Take-profit in an absolute price. In case of a sell signal (limit order) the TP must equal the price.",
    )
    sl: float = Field(
        ...,
        description="Mandatory. Stop-loss in an absolute price. In case of a sell signal (limit order) the SL must equal the price.",
    )
    position_size_in_percentage: float = Field(
        default=100,
        description="Caution, if one chooses another value than 100, the system will create a multi-position-trade (for scaling-in and scaling-out on a trade). In addition, one has to provide a provider_trade_id in order for the system to create a multi-position-trade. Any consecutive trades (scale-in/out), need to have provide the same provider_trade_id. Percentage of the trade position this algortihm is allowed to trade. Default is 100%, which is 1 position of your fund's positions. Another number than 100, will assume this trade has multiple positions. If a signal provider has one partial position open and then closes it, it will also regard the trade as fully closed.",
    )
    date_of_creation: int = Field(
        description="Mandatory. The UTC POSIX date/time when the signal was created in the signal provider's system. Use the POSIX UTC date format. "
    )

    @field_validator(
        "provider_id",
        "strategy_id",
        "provider_signal_id",
        "provider_trade_id",
        "market",
        "data_source",
    )
    def check_string_not_empty(cls, v):
        if not v or v.isspace():
            raise ValueError("This field must not be empty.")
        return v

    @field_validator("price", "tp", "sl", "position_size_in_percentage")
    def check_positive_value(cls, v):
        if v <= 0:
            raise ValueError("price must a positive number.")
        return v

    @field_validator("is_hot_signal")
    def check_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("is_hot_signal must be a boolean.")
        return v

    @field_validator("direction", "side")
    def check_enum(cls, v):
        if not isinstance(v, (Direction, Side)):
            raise ValueError("Invalid value for direction or side.")
        return v

    @field_validator("date_of_creation")
    def check_datetime(cls, v):
        if not isinstance(v, int):
            raise ValueError(f"date_of_creation must be an integer representing a POSIX timestamp in milliseconds, got type {type(v).__name__}")
        
        # # Assuming the value should be within a reasonable range, e.g., post-Unix epoch and not too far in the future
        # # Unix epoch starts at 1970-01-01, which is 0 in POSIX time
        # # Let's set an arbitrary upper limit for validation, e.g., January 1, 2030, for demonstration
        # min_timestamp = 0  # This would be the Unix epoch start
        # max_timestamp = 1893456000000  # Represents January 1, 2030, in milliseconds
        # if not (min_timestamp <= v <= max_timestamp):
        #     raise ValueError(f"date_of_creation must represent a date between 1970-01-01 and 2030-01-01, got {v}")

        # # The value passes the check, return it
        return v
