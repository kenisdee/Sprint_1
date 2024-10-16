import logging

import data_download as dd
import data_plotting as dplt

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    logging.info(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    logging.info(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    # Ввод тикера акции и периода
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    logging.info(f"Загрузка данных для тикера {ticker} за период {period}.")

    try:
        # Загрузка данных о акциях
        stock_data = dd.fetch_stock_data(ticker, period)
        logging.info("Данные успешно загружены.")

        # Добавление скользящего среднего к данным
        stock_data = dd.add_moving_average(stock_data)
        logging.info("Скользящее среднее успешно добавлено.")

        # Вычисление и вывод средней цены закрытия акций
        dd.calculate_and_display_average_price(stock_data)
        logging.info("Средняя цена закрытия вычислена и отображена.")

        # Построение графика данных
        dplt.create_and_save_plot(stock_data, ticker, period)
        logging.info("График успешно создан и сохранен.")

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()

