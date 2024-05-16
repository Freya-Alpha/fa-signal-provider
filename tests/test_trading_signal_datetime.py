from datetime import datetime, timezone
import time
import pytest
from fasignalprovider.direction import Direction
from fasignalprovider.side import Side
from fasignalprovider.trading_signal import TradingSignal  # Ensure to replace `your_module` with the actual name of your module

# Sample data for a valid TradingSignal, replace values as necessary
valid_data = {
    "provider_signal_id": "signal123",
    "provider_trade_id": "trade123",
    "provider_id": "provider123",
    "strategy_id": "strategy123",
    "market": "BTC/USDT",
    "data_source": "Binance",
    "direction": Direction.LONG,
    "side": Side.BUY,
    "price": 1000.0,
    "tp": 1200.0,
    "sl": 800.0,
    "position_size_in_percentage": 100,
    # "date_of_creation": This will be set in the tests
}

def test_trading_signal_accepts_posix_timestamp():
    # Test with integer POSIX timestamp, assuming milliseconds
    data_with_int = valid_data.copy()
    data_with_int["date_of_creation"] = int(time.time() * 1000)
    trading_signal = TradingSignal(**data_with_int)
    assert trading_signal.date_of_creation == data_with_int["date_of_creation"], "TradingSignal should accept integer POSIX timestamps including milliseconds"

