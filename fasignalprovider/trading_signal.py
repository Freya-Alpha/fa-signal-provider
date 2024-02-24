from pydantic import BaseModel, Field, field_validator
#from typing import Optional
from datetime import datetime
from fasignalprovider.direction import Direction
from fasignalprovider.side import Side


class TradingSignal(BaseModel):
    """
    A trading signal represents a suggestion to buy or sell. It is issued by a signal supplier
    (manually or algorithmically). It must have a correlating id to a trade.
    """

    provider_id: str = Field(
        ..., description="Mandatory. Your ID as a provider, who emitted the signal."
    )
    strategy_id: str = Field(
        ...,
        description="Mandatory. Provide the id of the strategy (you might have more than one algorithm), which is sending a signal.",
    )
    provider_trade_id: str = Field(
        ...,
        description="Mandatory. We describes a Trade as a buy and a sell (not soley a buy OR a sell). \
            Every trade is expected to consist of at least one buy signal (provider_signal_id) and at \
            least one sell signal (provider_signal_id).\
            Thus, the provider_trade_id is mandatory. This will allow to create a multi-position-trade. \
            E.g. one can send one long signal  with a provider_trade_id 77 and another long signal a \
            few hours later also with the provider_trade_id 77. Provided that the \
            position_size_in_percentage is less than 100 on the first one. All updates provided by the \
            system will hold the trade id.",
    )
    provider_signal_id: str = Field(
        ...,
        description="Mandatory. Provide us with your signal id. This correlation id is your own 'signal id' \
            of your internal system. Your and our party will use it to inspect process errors. \
            Do NOT mistaken this correlation id with the trade id.",
    )
    is_hot_signal: bool = Field(
        default=False,
        description="Mandatory. By DEFAULT, every signal is marked as a COLD SIGNAL.  \
            That is a paper-trading signal and will only be processed for forward-performance \
            testing. Hot signals are suggested to be processed by the order engines - \
            provided all other requirements for hot trading are fulfilled. Set this \
            value to true to suggest a hot trade.",
    )
    market: str = Field(..., description="Mandatory. The market you want to trade. e.g. BTC/USDT")
    data_source: str = Field(
        ...,
        description="Mandatory. The source of data you based your decision on. E.g. Binance, CoinMarketCap,\
            Chainlink, etc. This is to safeguard investments, which base on manipulated data sources.",
    )
    direction: Direction = Field(..., description="Mandatory. Simply LONG or SHORT.")
    side: Side = Field(
        ..., description="Mandatory. Simply BUY (open trade) or SELL (close trade)."
    )
    price: float = Field(
        ..., description="Mandatory. The price to buy or sell. Use for the limit-order or limit-stop-order"
    )
    tp: float = Field(..., description="Mandatory. Take-profit in absolute price.")
    sl: float = Field(..., description="Mandatory. Stop-loss in absolute price.")
    position_size_in_percentage: float = Field(
        default=100,
        description="Caution, if one chooses another value than 100, the system will create a multi-position-trade (for scaling-in and scaling-out on a trade). In addition, one has to provide a provider_trade_id in order for the system to create a multi-position-trade. Any consecutive trades (scale-in/out), need to have provide the same provider_trade_id. Percentage of the trade position this algortihm is allowed to trade. Default is 100%, which is 1 position of your fund's positions. Another number than 100, will assume this trade has multiple positions. If a signal provider has one partial position open and then closes it, it will also regard the trade as fully closed.",
    )
    date_of_creation: datetime = Field(
        default_factory=datetime.now,
        description="Mandatory. The UTC datetime when the signal was created in the signal provider's system.",
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
            raise ValueError("This field must not be empty")
        return v

    @field_validator("price", "tp", "sl", "position_size_in_percentage")
    def check_positive_value(cls, v):
        if v <= 0:
            raise ValueError("This field must be positive")
        return v

    @field_validator("is_hot_signal")
    def check_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("is_hot_signal must be a boolean")
        return v

    @field_validator("direction", "side")
    def check_enum(cls, v):
        if not isinstance(v, (Direction, Side)):
            raise ValueError("Invalid value for direction or side")
        return v

    @field_validator("date_of_creation")
    def check_datetime(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("date_of_creation must be a datetime object")
        return v
