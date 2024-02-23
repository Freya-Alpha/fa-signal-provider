from pydantic import ValidationError
import pytest
from datetime import datetime
from fasignalprovider.direction import Direction
from fasignalprovider.side import Side
from fasignalprovider.trading_signal import TradingSignal


def test_valid_trading_signal():
    # Test with valid data
    signal = TradingSignal(
        provider_id="provider123",
        strategy_id="strategy456",
        provider_trade_id="trade789",
        provider_signal_id="signal_id",
        market="BTC/USDT",
        data_source="Chainlink",
        direction=Direction.LONG,
        side=Side.BUY,
        price=10000.0,
        tp=10500.0,
        sl=9500.0,
        position_size_in_percentage=100,
        date_of_creation=datetime.now(),
    )
    assert signal is not None


# Parametrized tests for invalid data
@pytest.mark.parametrize(
    "provider_id, strategy_id, provider_trade_id, market, exchange, direction, side, price, tp, sl, position_size_in_percentage",
    [
        (
            "",
            "strategy456",
            "trade789",
            "BTC/USDT",
            "Binance",
            Direction.LONG,
            Side.BUY,
            10000.0,
            10500.0,
            9500.0,
            100,
        ),  # Empty provider_id
        (
            "provider123",
            "",
            "trade789",
            "BTC/USDT",
            "Binance",
            Direction.LONG,
            Side.BUY,
            10000.0,
            10500.0,
            9500.0,
            100,
        ),  # Empty strategy_id
    ],
)
def test_invalid_trading_signal(
    provider_id,
    strategy_id,
    provider_trade_id,
    market,
    exchange,
    direction,
    side,
    price,
    tp,
    sl,
    position_size_in_percentage,
):
    with pytest.raises(ValidationError):
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
            date_of_creation=datetime.now(),
        )

@pytest.mark.parametrize("price", [1, -100])
def test_negative_price(price):
    with pytest.raises(ValidationError):
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
            date_of_creation=datetime.now(),
        )

@pytest.mark.parametrize(
    "field,value",
    [
        ("price", 0),
        ("price", -100),
        ("tp", 0),
        ("tp", -100),
        ("sl", -0),
        ("sl", -100),
        ("position_size_in_percentage", 0),
        ("position_size_in_percentage", -100),
    ],
)
def test_negative_on_non_negative_numbers_only(field, value):
    kwargs = {
        "provider_id": "provider123",
        "strategy_id": "strategy456",
        "provider_trade_id": "trade789",
        "market": "BTC/USDT",
        "data_source": "Binance",
        "direction": Direction.LONG,
        "side": Side.BUY,
        "price": 10000.0,
        "tp": 10500.0,
        "sl": 9500.0,
        "position_size_in_percentage": 100,
        "date_of_creation": datetime.now(),
        "provider_signal_id": "signal123",  # Assuming this is a required field
    }

    kwargs[field] = value

    try:
        TradingSignal(**kwargs)
        # If no ValidationError is raised, explicitly fail the test.
        # This is crucial for the negative test logic where we expect every test case to raise an exception.
        pytest.fail(
            f"No ValidationError raised for {field} with value {value} for this negative test. \
                    Test should fail, because we don't allow positive (correct) values in this negative-test."
        )
    except ValidationError:
        # If a ValidationError is caught, it means the test behaves as expected, and this block can remain empty.
        pass
