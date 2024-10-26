import numpy as np
import pandas as pd
import yfinance as yf


def fetch_stock_data(ticker, period='1mo', start_date=None, end_date=None):
    """
    Загружает исторические данные о ценах акций с помощью библиотеки yfinance.

    :param ticker: Тикер акции (например, 'AAPL' для Apple Inc).
    :param period: Период данных (по умолчанию '1mo' для одного месяца).
    :param start_date: Дата начала в формате YYYY-MM-DD (опционально).
    :param end_date: Дата окончания в формате YYYY-MM-DD (опционально).
    :return: DataFrame с историческими данными о ценах акций.
    """
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if period not in valid_periods:
        raise ValueError(f"Период '{period}' невалиден, должен быть одним из {valid_periods}")

    try:
        stock = yf.Ticker(ticker)
        if start_date and end_date:
            data = stock.history(start=start_date, end=end_date)
        else:
            data = stock.history(period=period)

        if data.empty:
            raise ValueError(f"Данные для тикера {ticker} не найдены.")

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
        data['Ichimoku_Conversion'], data['Ichimoku_Base'], data['Ichimoku_Leading_Span_A'], data[
            'Ichimoku_Leading_Span_B'], data['Ichimoku_Lagging_Span'] = calculate_ichimoku_cloud(data)

        # Расчет стандартного отклонения
        data['Std_Deviation'] = calculate_std_deviation(data)

        # Расчет стандартного отклонения
        data['Std_Deviation'] = calculate_std_deviation(data)

        # Расчет среднего значения цены закрытия
        data['Mean_Closing_Price'] = calculate_mean_closing_price(data)

        # Расчет дисперсии цены закрытия
        data['Variance_Closing_Price'] = calculate_variance_closing_price(data)

        # Расчет коэффициента вариации
        data['Coefficient_of_Variation'] = calculate_coefficient_of_variation(data)

        return data
    except Exception as e:
        print(f"Ошибка при загрузке данных для тикера {ticker}: {e}")
        return pd.DataFrame()


def add_moving_average(data, window_size=5):
    """
    Добавляет скользящее среднее к данным о ценах акций.

    :param data: DataFrame с данными о ценах акций.
    :param window_size: Размер окна для скользящего среднего (по умолчанию 5).
    :return: DataFrame с добавленным столбцом 'Moving_Average'.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return data

    # Вычисление скользящего среднего для столбца 'Close'
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()

    return data


def calculate_rsi(data, period=14):
    """
    Рассчитывает индекс относительной силы (RSI).

    :param data: DataFrame с данными о ценах акций.
    :param period: Период для расчета RSI (по умолчанию 14).
    :return: Series с рассчитанным RSI.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series()

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """
    Рассчитывает индикатор MACD.

    :param data: DataFrame с данными о ценах акций.
    :param short_period: Короткий период для EMA (по умолчанию 12).
    :param long_period: Длинный период для EMA (по умолчанию 26).
    :param signal_period: Период для сигнальной линии (по умолчанию 9).
    :return: Два Series: MACD и сигнальная линия.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series(), pd.Series()

    short_ema = data['Close'].ewm(span=short_period, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_period, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, signal_line


def calculate_bollinger_bands(data, window=20, num_std=2):
    """
    Рассчитывает линии Боллинджера.

    :param data: DataFrame с данными о ценах акций.
    :param window: Размер окна для скользящего среднего (по умолчанию 20).
    :param num_std: Количество стандартных отклонений для расчета полос (по умолчанию 2).
    :return: Три Series: верхняя полоса, средняя полоса, нижняя полоса.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series(), pd.Series(), pd.Series()

    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band


def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
    """
    Рассчитывает стохастический осциллятор.

    :param data: DataFrame с данными о ценах акций.
    :param k_period: Период для %K (по умолчанию 14).
    :param d_period: Период для %D (по умолчанию 3).
    :return: Два Series: %K и %D.
    """
    if 'Low' not in data.columns or 'High' not in data.columns or 'Close' not in data.columns:
        print("Столбцы 'Low', 'High' или 'Close' отсутствуют в данных.")
        return pd.Series(), pd.Series()

    low_min = data['Low'].rolling(window=k_period).min()
    high_max = data['High'].rolling(window=k_period).max()
    k_percent = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    d_percent = k_percent.rolling(window=d_period).mean()
    return k_percent, d_percent


def calculate_vwap(data):
    """
    Рассчитывает средневзвешенную по объему цену (VWAP).

    :param data: DataFrame с данными о ценах акций.
    :return: Series с рассчитанным VWAP.
    """
    if 'Volume' not in data.columns or 'High' not in data.columns or 'Low' not in data.columns or 'Close' not in data.columns:
        print("Столбцы 'Volume', 'High', 'Low' или 'Close' отсутствуют в данных.")
        return pd.Series()

    vwap = (data['Volume'] * (data['High'] + data['Low'] + data['Close']) / 3).cumsum() / data['Volume'].cumsum()
    return vwap


def calculate_atr(data, period=14):
    """
    Рассчитывает средний истинный диапазон (ATR).

    :param data: DataFrame с данными о ценах акций.
    :param period: Период для расчета ATR (по умолчанию 14).
    :return: Series с рассчитанным ATR.
    """
    if 'High' not in data.columns or 'Low' not in data.columns or 'Close' not in data.columns:
        print("Столбцы 'High', 'Low' или 'Close' отсутствуют в данных.")
        return pd.Series()

    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr


def calculate_obv(data):
    """
    Рассчитывает накопленный объем (OBV).

    :param data: DataFrame с данными о ценах акций.
    :return: Series с рассчитанным OBV.
    """
    if 'Close' not in data.columns or 'Volume' not in data.columns:
        print("Столбцы 'Close' или 'Volume' отсутствуют в данных.")
        return pd.Series()

    obv = (np.sign(data['Close'].diff()) * data['Volume']).cumsum()
    return obv


def calculate_cci(data, period=20):
    """
    Рассчитывает индекс товарного канала (CCI).

    :param data: DataFrame с данными о ценах акций.
    :param period: Период для расчета CCI (по умолчанию 20).
    :return: Series с рассчитанным CCI.
    """
    if 'High' not in data.columns or 'Low' not in data.columns or 'Close' not in data.columns:
        print("Столбцы 'High', 'Low' или 'Close' отсутствуют в данных.")
        return pd.Series()

    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    sma = typical_price.rolling(window=period).mean()
    mad = typical_price.rolling(window=period).apply(lambda x: np.fabs(x - x.mean()).mean())
    cci = (typical_price - sma) / (0.015 * mad)
    return cci


def calculate_mfi(data, period=14):
    """
    Рассчитывает индекс денежного потока (MFI).

    :param data: DataFrame с данными о ценах акций.
    :param period: Период для расчета MFI (по умолчанию 14).
    :return: Series с рассчитанным MFI.
    """
    if 'High' not in data.columns or 'Low' not in data.columns or 'Close' not in data.columns or 'Volume' not in data.columns:
        print("Столбцы 'High', 'Low', 'Close' или 'Volume' отсутствуют в данных.")
        return pd.Series()

    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_flow = (money_flow.where(data['Close'] > data['Close'].shift(1), 0)).rolling(window=period).sum()
    negative_flow = (money_flow.where(data['Close'] < data['Close'].shift(1), 0)).rolling(window=period).sum()

    # Обработка случая, когда negative_flow равно нулю
    mfi = 100 - (100 / (1 + (positive_flow / negative_flow.replace(0, np.nan))))
    return mfi


def calculate_adl(data):
    """
    Рассчитывает накопленный объем (ADL).

    :param data: DataFrame с данными о ценах акций.
    :return: Series с рассчитанным ADL.
    """
    if 'Close' not in data.columns or 'Low' not in data.columns or 'High' not in data.columns or 'Volume' not in data.columns:
        print("Столбцы 'Close', 'Low', 'High' или 'Volume' отсутствуют в данных.")
        return pd.Series()

    mfm = ((data['Close'] - data['Low']) - (data['High'] - data['Close'])) / (data['High'] - data['Low'])
    mfv = mfm * data['Volume']
    adl = mfv.cumsum()
    return adl


def calculate_parabolic_sar(data, acceleration=0.02, max_acceleration=0.2):
    """
    Рассчитывает параболический SAR.

    :param data: DataFrame с данными о ценах акций.
    :param acceleration: Фактор ускорения (по умолчанию 0.02).
    :param max_acceleration: Максимальный фактор ускорения (по умолчанию 0.2).
    :return: Series с рассчитанным SAR.
    """
    if 'Close' not in data.columns or 'Low' not in data.columns or 'High' not in data.columns:
        print("Столбцы 'Close', 'Low' или 'High' отсутствуют в данных.")
        return pd.Series()

    sar = data['Close'].copy()
    trend = np.zeros(len(data))
    extreme_point = data['High'].copy()
    acceleration_factor = acceleration

    for i in range(1, len(data)):
        if trend[i - 1] == 0:  # Если тренд был нисходящим
            sar.iloc[i] = sar.iloc[i - 1] + acceleration_factor * (extreme_point.iloc[i - 1] - sar.iloc[i - 1])
            if data['Low'].iloc[i] < sar.iloc[i]:
                sar.iloc[i] = data['Low'].iloc[i]
                trend[i] = 1  # Переключение на восходящий тренд
                extreme_point.iloc[i] = data['High'].iloc[i]
                acceleration_factor = acceleration
            else:
                trend[i] = 0
                if data['High'].iloc[i] > extreme_point.iloc[i - 1]:
                    extreme_point.iloc[i] = data['High'].iloc[i]
                    acceleration_factor = min(acceleration_factor + acceleration, max_acceleration)
                else:
                    extreme_point.iloc[i] = extreme_point.iloc[i - 1]
        else:  # Если тренд был восходящим
            sar.iloc[i] = sar.iloc[i - 1] + acceleration_factor * (extreme_point.iloc[i - 1] - sar.iloc[i - 1])
            if data['High'].iloc[i] > sar.iloc[i]:
                sar.iloc[i] = data['High'].iloc[i]
                trend[i] = 0  # Переключение на нисходящий тренд
                extreme_point.iloc[i] = data['Low'].iloc[i]
                acceleration_factor = acceleration
            else:
                trend[i] = 1
                if data['Low'].iloc[i] < extreme_point.iloc[i - 1]:
                    extreme_point.iloc[i] = data['Low'].iloc[i]
                    acceleration_factor = min(acceleration_factor + acceleration, max_acceleration)
                else:
                    extreme_point.iloc[i] = extreme_point.iloc[i - 1]

    return sar


def calculate_ichimoku_cloud(data, conversion_period=9, base_period=26, leading_span_b_period=52,
                             lagging_span_period=26):
    """
    Рассчитывает облако Ишимоку.

    :param data: DataFrame с данными о ценах акций.
    :param conversion_period: Период для линии преобразования (по умолчанию 9).
    :param base_period: Период для базовой линии (по умолчанию 26).
    :param leading_span_b_period: Период для второй линии опережения (по умолчанию 52).
    :param lagging_span_period: Период для линии запаздывания (по умолчанию 26).
    :return: Пять Series: линия преобразования, базовая линия, первая линия опережения, вторая линия опережения, линия запаздывания.
    """
    if 'High' not in data.columns or 'Low' not in data.columns or 'Close' not in data.columns:
        print("Столбцы 'High', 'Low' или 'Close' отсутствуют в данных.")
        return pd.Series(), pd.Series(), pd.Series(), pd.Series(), pd.Series()

    conversion_line = (data['High'].rolling(window=conversion_period).max() + data['Low'].rolling(
        window=conversion_period).min()) / 2
    base_line = (data['High'].rolling(window=base_period).max() + data['Low'].rolling(window=base_period).min()) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (data['High'].rolling(window=leading_span_b_period).max() + data['Low'].rolling(
        window=leading_span_b_period).min()) / 2
    lagging_span = data['Close'].shift(-lagging_span_period)
    return conversion_line, base_line, leading_span_a, leading_span_b, lagging_span


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций, дисперсию цены закрытия и коэффициент вариации.

    :param data: DataFrame с данными о ценах акций.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return

    if data['Close'].empty:
        print("Столбец 'Close' пуст.")
        return

    mean_closing_price = data['Close'].mean()
    variance_closing_price = data['Close'].var()
    std_deviation = data['Close'].std()
    coefficient_of_variation = (std_deviation / mean_closing_price) * 100

    print(f"Средняя цена закрытия акций: {mean_closing_price:.2f}")
    print(f"Дисперсия цены закрытия: {variance_closing_price:.2f}")
    print(f"Коэффициент вариации: {coefficient_of_variation:.2f}%")


def export_data_to_csv(data, filename):
    """
    Экспортирует данные об акциях в CSV файл.

    :param data: DataFrame с данными о ценах акций.
    :param filename: Имя файла для сохранения данных.
    """
    if data.empty:
        print("Данные пусты.")
        return

    data.to_csv(filename)
    print(f"Данные успешно экспортированы в файл {filename}")


def calculate_std_deviation(data, window=20):
    """
    Рассчитывает стандартное отклонение цены закрытия.

    :param data: DataFrame с данными о ценах акций.
    :param window: Размер окна для расчета стандартного отклонения (по умолчанию 20).
    :return: Series с рассчитанным стандартным отклонением.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series()

    std_deviation = data['Close'].rolling(window=window).std()
    return std_deviation


def calculate_mean_closing_price(data):
    """
    Рассчитывает среднее значение цены закрытия.

    :param data: DataFrame с данными о ценах акций.
    :return: Series с рассчитанным средним значением.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series()

    mean_closing_price = data['Close'].mean()
    return mean_closing_price


def calculate_variance_closing_price(data):
    """
    Рассчитывает дисперсию цены закрытия.

    :param data: DataFrame с данными о ценах акций.
    :return: Series с рассчитанной дисперсией.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series()

    variance_closing_price = data['Close'].var()
    return variance_closing_price


def calculate_coefficient_of_variation(data):
    """
    Рассчитывает коэффициент вариации цены закрытия.

    :param data: DataFrame с данными о ценах акций.
    :return: Series с рассчитанным коэффициентом вариации.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return pd.Series()

    mean_closing_price = data['Close'].mean()
    std_deviation = data['Close'].std()
    coefficient_of_variation = (std_deviation / mean_closing_price) * 100
    return coefficient_of_variation


def calculate_correlation_between_closing_prices(data1, data2):
    """
    Рассчитывает корреляцию между ценами закрытия двух разных акций.

    :param data1: DataFrame с данными о ценах первой акции.
    :param data2: DataFrame с данными о ценах второй акции.
    :return: Коэффициент корреляции.
    """
    if 'Close' not in data1.columns or 'Close' not in data2.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return None

    correlation = data1['Close'].corr(data2['Close'])
    return correlation
