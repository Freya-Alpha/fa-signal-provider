from pydantic import BaseModel, Field
from datetime import datetime
from typing import TypeVar, Optional
T = TypeVar('T')


class Payload(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Event(Payload):
    eventType: str

class Error(BaseModel):
    code: int
    message: str
    type: Optional[str] = None

### TECHNICAL EVENTS FROM HERE DOWNWARDS ###

class ErrorEvent(Event):
    """An error Event is thrown in case of technical event. e.g.
    FastAPI Middleware fails, wrong headers, false authentication,
    etc."""
    error: Error
    eventType: str = "ErrorEvent"

### BUSINESS EVENTS FROM HERE DOWNWARDS ###

class SignalReceived(Event):
    internal_signal_id: str
    eventType: str = "SignalReceived"

class SignalRejected(Event):
    submitted_signal_id: str
    reason: str
    eventType: str = "SignalRejected"    

class SignalQualified(Event):
    signal_id: str
    time_of_qualification: datetime
    eventType: str = "SignalQualified"

class TradeCreated(Event):
    trade_id: str
    details: dict  # You can replace 'dict' with a more specific model if you have one
    eventType: str = "TradeCreated"

class OrderCreated(Event):
    order_id: str
    order_details: dict  # Replace 'dict' with a specific model as needed
    eventType: str = "OrderCreated"

class OrderFilled(Event):
    order_id: str
    fill_details: dict  # Replace 'dict' with a specific model as needed
    eventType: str = "OrderFilled"

class OrderCanceled(Event):
    order_id: str
    cancellation_reason: Optional[str] = None
    eventType: str = "OrderCanceled"

class ProfitTaken(Event):
    trade_id: str
    profit_amount: float
    eventType: str = "ProfitTaken"

