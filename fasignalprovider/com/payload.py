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
    code: Optional[Code]

    def serialize(self) -> Dict[str, Any]:
        data = super().serialize()
        data.update({
            "event_type": self.event_type,
            "code": self.code.value if self.code else None,
        })
        return data

### TECHNICAL EVENTS FROM HERE DOWNWARDS ###
class ErrorEvent(Event):
    """An error Event is thrown in case of technical event. e.g.
    FastAPI Middleware fails, wrong headers, false authentication,
    etc."""

    event_type: str = "ErrorEvent"
    detail: Optional[str] = None


### BUSINESS EVENTS FROM HERE DOWNWARDS ###
class SignalReceived(Event):
    internal_signal_id: str
    event_type: str = "SignalReceived"


class SignalRejected(Event):
    submitted_signal_id: str
    reason: str
    event_type: str = "SignalRejected"


class SignalQualified(Event):
    signal_id: str
    time_of_qualification: datetime
    event_type: str = "SignalQualified"


class TradeCreated(Event):
    trade_id: str
    details: dict  # You can replace 'dict' with a more specific model if you have one
    event_type: str = "TradeCreated"


class OrderCreated(Event):
    order_id: str
    order_details: dict  # Replace 'dict' with a specific model as needed
    event_type: str = "OrderCreated"


class OrderFilled(Event):
    order_id: str
    fill_details: dict  # Replace 'dict' with a specific model as needed
    event_type: str = "OrderFilled"


class OrderCanceled(Event):
    order_id: str
    cancellation_reason: Optional[str] = None
    event_type: str = "OrderCanceled"


class ProfitTaken(Event):
    trade_id: str
    profit_amount: float
    event_type: str = "ProfitTaken"
