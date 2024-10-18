import data_download as dd
import data_plotting as dplt


def notify_if_strong_fluctuations(data, threshold):
    """
    Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

    :param data: DataFrame с данными о ценах закрытия акций.
    :param threshold: Порог колебаний в процентах.
    """
    # Проверка наличия столбца 'Close' в данных
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return

    # Проверка на пустые данные
    if data.empty:
        print("Данные пусты.")
        return

    # Вычисление максимальной и минимальной цены закрытия
    max_price = data['Close'].max()
    min_price = data['Close'].min()

    # Вычисление процента колебаний
    fluctuation = ((max_price - min_price) / min_price) * 100

    # Уведомление о сильных колебаниях или их отсутствии
    if fluctuation > threshold:
        print(f"Обнаружены сильные колебания цены акций: {fluctuation:.2f}% (порог: {threshold}%)")
    else:
        print(f"Колебания цены акций в пределах нормы: {fluctuation:.2f}% (порог: {threshold}%)")


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    # Ввод тикера акции и периода
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Ввод порога колебаний
    threshold = float(input("Введите порог колебаний в процентах (например, '10' для 10%): "))

    try:
        # Загрузка данных о акциях
        stock_data = dd.fetch_stock_data(ticker, period)

        # Проверка на пустые данные
        if stock_data.empty:
            print("Загруженные данные пусты.")
            return

        # Добавление скользящего среднего к данным
        stock_data = dd.add_moving_average(stock_data)

        # Вычисление и вывод средней цены закрытия акций
        dd.calculate_and_display_average_price(stock_data)

        # Уведомление о сильных колебаниях цены акций
        notify_if_strong_fluctuations(stock_data, threshold)

        # Построение графика данных
        dplt.create_and_save_plot(stock_data, ticker, period)

    except ValueError as ve:
        print(f"Ошибка ввода данных: {ve}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
