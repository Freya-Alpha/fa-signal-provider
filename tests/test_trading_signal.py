import pytest
from datetime import datetime
from fasignalprovider.direction import Direction
from fasignalprovider.side import Side
from fasignalprovider.trading_signal import TradingSignal  # Replace 'your_module' with the actual name of your module

def test_valid_trading_signal():
    # Test with valid data
    signal = TradingSignal(
        provider_id="provider123",
        strategy_id="strategy456",
        provider_trade_id="trade789",
        market="BTC/USDT",
        exchange="Binance",
        direction=Direction.LONG,
        side=Side.BUY,
        price=10000.0,
        tp=10500.0,
        sl=9500.0,
        position_size_in_percentage=100,
        date_of_creation=datetime.now()
    )
    assert signal is not None

# Parametrized tests for invalid data
@pytest.mark.parametrize("provider_id, strategy_id, provider_trade_id, market, exchange, direction, side, price, tp, sl, position_size_in_percentage", [
    ("", "strategy456", "trade789", "BTC/USDT", "Binance", Direction.LONG, Side.BUY, 10000.0, 10500.0, 9500.0, 100),  # Empty provider_id
    ("provider123", "", "trade789", "BTC/USDT", "Binance", Direction.LONG, Side.BUY, 10000.0, 10500.0, 9500.0, 100),  # Empty strategy_id
    # ... Add more test cases as needed ...
])
def test_invalid_trading_signal(provider_id, strategy_id, provider_trade_id, market, exchange, direction, side, price, tp, sl, position_size_in_percentage):
    with pytest.raises(ValueError):
        TradingSignal(
            provider_id=provider_id,
            strategy_id=strategy_id,
            provider_trade_id=provider_trade_id,
            market=market,
            exchange=exchange,
            direction=direction,
            side=side,
            price=price,
            tp=tp,
            sl=sl,
            position_size_in_percentage=position_size_in_percentage,
            date_of_creation=datetime.now()
        )

# Additional tests for specific validations
# For example, testing negative price, tp, or sl
@pytest.mark.parametrize("price", [0, -100])
def test_negative_price(price):
    with pytest.raises(ValueError):
        TradingSignal(
            provider_id="provider123",
            strategy_id="strategy456",
            provider_trade_id="trade789",
            market="BTC/USDT",
            exchange="Binance",
            direction=Direction.LONG,
            side=Side.BUY,
            price=price,
            tp=10500.0,
            sl=9500.0,
            position_size_in_percentage=100,
            date_of_creation=datetime.now()
        )

# ... Add more tests for other validations ...
