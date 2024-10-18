import yfinance as yf


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
