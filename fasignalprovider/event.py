from abc import ABC
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import time
from typing import Any, ClassVar, Dict, TypeVar, Optional
from fasignalprovider.code import Code
from fasignalprovider.trading_signal import TradingSignal

T = TypeVar("T")


class Event(BaseModel):
    event_timestamp: int = Field(
        default_factory=lambda: int(time.time() * 1000)
    )
    event_type: ClassVar[str]
    detail: Optional[str] = None
    data: Optional[Dict[str, Any]] = None  # with type hints
    """Data is used to store the object value. e.g. a signal, a trade, a profit, etc."""

    def serialize(self) -> Dict[str, Any]:
        data = {
            "event_type": self.event_type,
            "detail": self.detail,
            "data": self._serialize_data(self.data),
        }
        # Optionally, you can remove keys with None values if you don't want them in the serialized output
        # return {k: v for k, v in data.items() if v is not None}
        return data

    def _serialize_data(
        self, data: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if data is None:
            return None
        # Serialize each value in the dictionary, converting datetime to ISO format if necessary
        return {key: self._serialize_value(value) for key, value in data.items()}

    def _serialize_value(self, value: Any) -> Any:
        if isinstance(value, datetime):
            # Convert datetime to ISO format string
            return value.astimezone().isoformat()
        elif isinstance(value, dict):
            # Recursively serialize dictionary values
            return self._serialize_data(value)
        return value


### TECHNICAL EVENTS FROM HERE DOWNWARDS ###
class ErrorEvent(Event):
    """An error Event is sent in case of any technical events. e.g.
    webservice middleware fails, wrong headers, false authentication,
    etc."""

    event_type: ClassVar[str] = "error_event"
    code: Optional[Code]

    def serialize(self) -> Dict[str, Any]:
        data = super().serialize()
        data.update(
            {
                "event_type": self.event_type,
                "code": self.code.value if self.code else None,
            }
        )
        # Optionally, you can remove keys with None values if you don't want them in the serialized output
        # return {k: v for k, v in data.items() if v is not None}
        return data


### BUSINESS EVENTS FROM HERE DOWNWARDS ###


######## TRADING SIGNAL EVENTS ########
class TradingSignalDataInvalidated(Event):
    """This event occures when input data is syntactically invalid to represent a Trading Signal."""

    signal_data: str
    """Whatever data this is."""
    ip: str
    event_type: ClassVar[str] = "trading_signal_data_invalidated"
    reason_for_invalidation: str


class TradingSignalIncoming(Event):
    """This event occures when a trading signal contains syntactically valid Trading Signal data, but has not yet been completely syntactically verified and stored."""
    signal_data: Dict
    ip: str
    event_type: ClassVar[str] = "trading_signal_incoming"


class TradingSignalEvent(Event, ABC):
    """ABSTRACT - This is the base of all signal events."""
    trading_signal: TradingSignal


class TradingSignalReceived(TradingSignalEvent):
    """This is when a trading signal was received without errors."""
    internal_signal_id: str
    event_type: ClassVar[str] = "trading_signal_received"
    ip: str
    date_of_reception: str = Field(
        default_factory=lambda: int(time.time() * 1000)
    )


class ReasonForRejection(str, Enum):
    NOT_AUTHENTICATED = "not_authenticated"
    SCAM = "scam"
    DOS_ATTACK = (
        "dos_attack"  # any flood attack: slowloris, ping-of-death, query attack, etc.
    )
    BANNED_SUPPLIER = "banned_supplier"
    BANNED_STRATEGY = "banned_strategy"
    BANNED_IP = "banned_ip"
    MARKET_NOT_ALLOWED = "market_not_allowed"
    INVALID_DATA = "invalid_data"
    INVALID_PRICE = "invalid_price"
    INCLOMPLETE = "incomplete"  # any kind of missing data


class TradingSignalRejected(TradingSignalReceived):
    """This is when a trading signal was deliberately rejected after the qualification process has been completed. It is semantically rejected."""

    provider_signal_id: str
    reasons_for_rejection: set[ReasonForRejection]
    event_type: ClassVar[str] = "signal_rejected"
    date_of_rejection: str = Field(
        default_factory=lambda: int(time.time() * 1000)
    )

    @classmethod
    def from_raw_signal(
        cls,
        raw_signal: TradingSignalReceived,
        reasons_for_rejection: ReasonForRejection,
    ):
        # Ensure the reason for rejection is provided
        rejected_signal = cls(
            **raw_signal.model_dump(), reasons_for_rejection=reasons_for_rejection
        )
        return rejected_signal


class ReasonForCold(str, Enum):
    PROVIDER_NOT_ELIGABLE_FOR_HOT_SIGNAL = "provider_not_eligable_for_hot_signal"
    STRATEGY_NOT_QUALIFIED = (
        "strategy_not_qualified"  # But is allowed to send cold signals instead.
    )
    DISQUALIFIED_STRATEGY = "disqualified_strategy"  # This strategy used to be qualified. Stil allowed to send cold to redeem status.
    SYSTEM_IS_COLD = "system_is_cold"  # The system is cold.
    SIGNAL_MARKED_COLD = (
        "signal_marked_cold"  # The signal was marked cold by the provider
    )


class TradingSignalQualified(TradingSignalReceived, ABC):
    """ABSTRACT - This event appears if a trading signal has successfully qualified. It is semantically correct."""

    event_type: ClassVar[str] = "trading_signal_qualified"
    date_of_qualification: str = Field(
        default_factory=lambda: int(time.time() * 1000)
    )

    def __init__(self, **data):
        if "time_of_qualification" in data:
            # Ensure the provided datetime is in UTC
            data["time_of_qualification"] = data["time_of_qualification"].astimezone(
                tz=timezone.utc
            )
        super().__init__(**data)


class TradingSignalQualifiedHot(TradingSignalQualified):
    event_type: ClassVar[str] = "trading_signal_qualified_hot"


class TradingSignalQualifiedCold(TradingSignalQualified):
    event_type: ClassVar[str] = "trading_signal_qualified_cold"
    reasons_for_cold: set[ReasonForCold]


######## TRADE EVENTS ########


class TradeCreated(Event):
    """This event appears if a trade base on a signal was started. With us a trade consists of at least one buy and one sell signal (or TP/SL)."""

    trade_id: str
    event_type: ClassVar[str] = "trade_created"


class TradeCanceled(Event):
    """This event occures if a Trade has been canceled. Either with no fill or partial fill."""

    trade_id: str
    reason: str
    event_type: ClassVar[str] = "trade_canceled"


class TradeFinished(Event):
    trade_id: str
    event_type: ClassVar[str] = "trade_finished"


class OrderCreated(Event):
    order_id: str
    event_type: ClassVar[str] = "order_created"


class OrderFilled(Event):
    order_id: str
    event_type: ClassVar[str] = "order_filled"


class OrderCanceled(Event):
    order_id: str
    reason: Optional[str] = None
    event_type: ClassVar[str] = "order_canceled"


class ProfitTaken(Event):
    trade_id: str
    profit_amount: float
    event_type: ClassVar[str] = "profit_taken"
