import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(ticker, period='1mo'):
    """
    Загружает исторические данные о ценах акций с помощью библиотеки yfinance.

    :param ticker: Тикер акции (например, 'AAPL' для Apple Inc).
    :param period: Период данных (по умолчанию '1mo' для одного месяца).
    :return: DataFrame с историческими данными о ценах акций.
    """
    # Создание объекта Ticker для указанного тикера
    stock = yf.Ticker(ticker)

    # Загрузка исторических данных за указанный период
    data = stock.history(period=period)

    # Добавление скользящего среднего
    data = add_moving_average(data)

    # Расчет RSI
    data['RSI'] = calculate_rsi(data)

    # Расчет MACD
    data['MACD'], data['Signal'] = calculate_macd(data)

    # Расчет Bollinger Bands
    data['Bollinger_Upper'], data['Bollinger_Middle'], data['Bollinger_Lower'] = calculate_bollinger_bands(data)

    # Расчет Stochastic Oscillator
    data['Stochastic_K'], data['Stochastic_D'] = calculate_stochastic_oscillator(data)

    # Расчет VWAP
    data['VWAP'] = calculate_vwap(data)

    # Расчет ATR
    data['ATR'] = calculate_atr(data)

    # Расчет OBV
    data['OBV'] = calculate_obv(data)

    # Расчет CCI
    data['CCI'] = calculate_cci(data)

    # Расчет MFI
    data['MFI'] = calculate_mfi(data)

    # Расчет ADL
    data['ADL'] = calculate_adl(data)

    # Расчет Parabolic SAR
    data['Parabolic_SAR'] = calculate_parabolic_sar(data)

    # Расчет Ichimoku Cloud
    data['Ichimoku_Conversion'], data['Ichimoku_Base'], data['Ichimoku_Leading_Span_A'], data['Ichimoku_Leading_Span_B'], data['Ichimoku_Lagging_Span'] = calculate_ichimoku_cloud(data)

    return data

def add_moving_average(data, window_size=5):
    """
    Добавляет скользящее среднее к данным о ценах акций.

    :param data: DataFrame с данными о ценах акций.
    :param window_size: Размер окна для скользящего среднего (по умолчанию 5).
    :return: DataFrame с добавленным столбцом 'Moving_Average'.
    """
    # Вычисление скользящего среднего для столбца 'Close'
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()

    return data

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    short_ema = data['Close'].ewm(span=short_period, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_period, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, signal_line

def calculate_bollinger_bands(data, window=20, num_std=2):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band

def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
    low_min = data['Low'].rolling(window=k_period).min()
    high_max = data['High'].rolling(window=k_period).max()
    k_percent = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    d_percent = k_percent.rolling(window=d_period).mean()
    return k_percent, d_percent

def calculate_vwap(data):
    vwap = (data['Volume'] * (data['High'] + data['Low'] + data['Close']) / 3).cumsum() / data['Volume'].cumsum()
    return vwap

def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

def calculate_obv(data):
    obv = (np.sign(data['Close'].diff()) * data['Volume']).cumsum()
    return obv

def calculate_cci(data, period=20):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    sma = typical_price.rolling(window=period).mean()
    mad = typical_price.rolling(window=period).apply(lambda x: np.fabs(x - x.mean()).mean())
    cci = (typical_price - sma) / (0.015 * mad)
    return cci

def calculate_mfi(data, period=14):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_flow = (money_flow.where(data['Close'] > data['Close'].shift(1), 0)).rolling(window=period).sum()
    negative_flow = (money_flow.where(data['Close'] < data['Close'].shift(1), 0)).rolling(window=period).sum()
    mfi = 100 - (100 / (1 + (positive_flow / negative_flow)))
    return mfi

def calculate_adl(data):
    mfm = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
    mfv = mfm * data['Volume']
    adl = mfv.cumsum()
    return adl

def calculate_parabolic_sar(data, acceleration=0.02, max_acceleration=0.2):
    sar = data['Close'].copy()
    trend = np.zeros(len(data))
    extreme_point = data['High'].copy()
    acceleration_factor = acceleration

    for i in range(1, len(data)):
        if trend[i-1] == 0:  # Если тренд был нисходящим
            sar.iloc[i] = sar.iloc[i-1] + acceleration_factor * (extreme_point.iloc[i-1] - sar.iloc[i-1])
            if data['Low'].iloc[i] < sar.iloc[i]:
                sar.iloc[i] = data['Low'].iloc[i]
                trend[i] = 1  # Переключение на восходящий тренд
                extreme_point.iloc[i] = data['High'].iloc[i]
                acceleration_factor = acceleration
            else:
                trend[i] = 0
                if data['High'].iloc[i] > extreme_point.iloc[i-1]:
                    extreme_point.iloc[i] = data['High'].iloc[i]
                    acceleration_factor = min(acceleration_factor + acceleration, max_acceleration)
                else:
                    extreme_point.iloc[i] = extreme_point.iloc[i-1]
        else:  # Если тренд был восходящим
            sar.iloc[i] = sar.iloc[i-1] + acceleration_factor * (extreme_point.iloc[i-1] - sar.iloc[i-1])
            if data['High'].iloc[i] > sar.iloc[i]:
                sar.iloc[i] = data['High'].iloc[i]
                trend[i] = 0  # Переключение на нисходящий тренд
                extreme_point.iloc[i] = data['Low'].iloc[i]
                acceleration_factor = acceleration
            else:
                trend[i] = 1
                if data['Low'].iloc[i] < extreme_point.iloc[i-1]:
                    extreme_point.iloc[i] = data['Low'].iloc[i]
                    acceleration_factor = min(acceleration_factor + acceleration, max_acceleration)
                else:
                    extreme_point.iloc[i] = extreme_point.iloc[i-1]

    return sar

def calculate_ichimoku_cloud(data, conversion_period=9, base_period=26, leading_span_b_period=52, lagging_span_period=26):
    conversion_line = (data['High'].rolling(window=conversion_period).max() + data['Low'].rolling(window=conversion_period).min()) / 2
    base_line = (data['High'].rolling(window=base_period).max() + data['Low'].rolling(window=base_period).min()) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (data['High'].rolling(window=leading_span_b_period).max() + data['Low'].rolling(window=leading_span_b_period).min()) / 2
    lagging_span = data['Close'].shift(-lagging_span_period)
    return conversion_line, base_line, leading_span_a, leading_span_b, lagging_span

def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций.

    :param data: DataFrame с данными о ценах акций.
    """
    # Проверка наличия столбца 'Close' в данных
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return

    # Вычисление средней цены закрытия
    average_price = data['Close'].mean()

    # Вывод средней цены закрытия
    print(f"Средняя цена закрытия акций: {average_price:.2f}")

def export_data_to_csv(data, filename):
    """
    Экспортирует данные об акциях в CSV файл.

    :param data: DataFrame с данными о ценах акций.
    :param filename: Имя файла для сохранения данных.
    """
    # Сохранение данных в CSV файл
    data.to_csv(filename)

    # Вывод сообщения о том, что данные сохранены
    print(f"Данные успешно экспортированы в файл {filename}")