from datetime import datetime, timezone
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

def test_trading_signal_with_z_version():
    # Test with 'Z' version of datetime
    data_with_z = valid_data.copy()
    data_with_z["date_of_creation"] = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    trading_signal = TradingSignal(**data_with_z)
    assert trading_signal.date_of_creation == data_with_z["date_of_creation"], "TradingSignal should accept datetime strings with 'Z'"

