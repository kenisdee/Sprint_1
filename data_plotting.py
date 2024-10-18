import matplotlib.pyplot as plt
import pandas as pd



def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создает и сохраняет график цены акций с течением времени.

    :param data: DataFrame с данными о ценах закрытия и скользящем среднем.
    :param ticker: Тикер акции.
    :param period: Период данных.
    :param filename: Имя файла для сохранения графика (по умолчанию генерируется автоматически).
    """
    # Создание фигуры для графика
    plt.figure(figsize=(10, 6))

    # Проверка наличия столбца 'Date' в данных
    if 'Date' not in data:
        # Если 'Date' отсутствует, проверяем индекс на тип datetime
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        # Если 'Date' присутствует, проверяем его на тип datetime
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    # Настройка заголовка и меток осей
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # Генерация имени файла, если оно не было предоставлено
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    # Сохранение графика в файл
    plt.savefig(filename)
    print(f"График сохранен как {filename}")
