from pydantic import BaseModel, Field
from datetime import datetime, timezone
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
    data: Optional[Dict[str, Any]] = None  # with type hints
    """Data is used to store the object value. e.g. a signal, a trade, a profit, etc."""

    def serialize(self) -> Dict[str, Any]:
        data = super().serialize()
        data.update(
            {
                "event_type": self.event_type,
                "detail": self.detail,
                "code": self.code.value if self.code else None,
                "data": self._serialize_data(self.data)
            }
        )
        # Optionally, you can remove keys with None values if you don't want them in the serialized output
        #return {k: v for k, v in data.items() if v is not None}
        return data
    
    def _serialize_data(self, data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
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
    event_type: str = "error_event"


### BUSINESS EVENTS FROM HERE DOWNWARDS ###
    
class SignalIncoming(Event):
    """This event occures when a trading signal is incoming, but has not yet been completely received and stored."""        
    signal_data: Dict
    event_type: str = "signal_incoming"

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
    """This event appears if a trading signal has successfully qualified."""
    signal_id: str
    time_of_qualification: datetime = Field(default_factory=lambda: datetime.utcnow())
    event_type: str = "signal_qualified"

    def __init__(self, **data):
        if 'time_of_qualification' in data:
            # Ensure the provided datetime is in UTC
            data['time_of_qualification'] = data['time_of_qualification'].astimezone(tz=timezone.utc)
        super().__init__(**data)

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
