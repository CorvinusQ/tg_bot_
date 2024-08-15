# config.py

TRADE_CONFIG = {
    'default': {
        'position_size': 0.01,  # Размер позиции
        'leverage': 10,          # Плечо
        'stop_loss': 50,         # Стоп-лосс в пунктах
        'take_profit': 100,      # Тейк-профит в пунктах
    },
    'BTCUSDT': {
        'position_size': 0.02,
        'leverage': 20,
        'stop_loss': 40,
        'take_profit': 80,
    },
    'ETHUSDT': {
        'position_size': 0.1,
        'leverage': 15,
        'stop_loss': 30,
        'take_profit': 60,
    }
}
