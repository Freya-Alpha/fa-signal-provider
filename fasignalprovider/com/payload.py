from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, TypeVar, Optional
from fasignalprovider.com.code import Code

T = TypeVar("T")

class Payload(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    def serialize(self) -> Dict[str, Any]:
        # Since this is the top-level class, we'll manually construct the dictionary
        # Pydantic's `dict()` method can be used here to convert model to dict
        return self.model_dump()


class Event(Payload):
    event_type: str
    detail: Optional[str] = None
    code: Optional[Code]

    def serialize(self) -> Dict[str, Any]:
        data = super().serialize()
        data.update(
            {
                "event_type": self.event_type,
                "detail": self.detail,
                "code": self.code.value if self.code else None,
            }
        )
        return data


### TECHNICAL EVENTS FROM HERE DOWNWARDS ###
class ErrorEvent(Event):
    """An error Event is sent in case of any technical events. e.g.
    webservice middleware fails, wrong headers, false authentication,
    etc."""
    event_type: str = "error_event"


### BUSINESS EVENTS FROM HERE DOWNWARDS ###
    
class SignalSubmitted(Event):
    """This event occures when a trading signal has been submitted to us, but has not yet been completely received and stored."""
    internal_signal_id: str
    event_type: str = "signal_submitted"


class SignalReceived(Event):
    """This is when a trading signal was received without errors."""
    internal_signal_id: str
    event_type: str = "signal_received"


class SignalRejected(Event):
    """This is when a trading signal was deliberately rejected after the qualification process has been completed."""
    submitted_signal_id: str
    reason: str
    event_type: str = "signal_rejected"


class SignalQualified(Event):
    """This event appears if a trading signals has successfully qualified."""
    signal_id: str
    time_of_qualification: datetime
    event_type: str = "signal_qualified"

class TradeCreated(Event):
    """This event appears if a trade base on a signal was started. With us a trade consists of at least one buy and one sell signal (or TP/SL)."""
    trade_id: str
    event_type: str = "trade_created"

class TradeCanceled(Event):
    trade_id: str
    reason: str
    event_type: str = "trade_canceled"

class TradeFinished(Event):
    trade_id: str
    event_type: str = "trade_finished"


class OrderCreated(Event):
    order_id: str
    event_type: str = "order_created"


class OrderFilled(Event):
    order_id: str
    event_type: str = "order_filled"


class OrderCanceled(Event):
    order_id: str
    reason: Optional[str] = None
    event_type: str = "order_canceled"


class ProfitTaken(Event):
    trade_id: str
    profit_amount: float
    event_type: str = "profit_taken"
