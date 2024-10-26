import os
import matplotlib.pyplot as plt
import data_download as dd
import data_plotting as dplt

def create_styles_file():
    """
    Создает файл styles.txt и записывает в него список доступных стилей.
    """
    styles_file = 'styles.txt'
    if not os.path.exists(styles_file):
        with open(styles_file, 'w') as file:
            for style in plt.style.available:
                file.write(f"{style}\n")

def notify_if_strong_fluctuations(data, threshold):
    """
    Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

    :param data: DataFrame с данными о ценах закрытия акций.
    :param threshold: Порог колебаний в процентах.
    """
    if 'Close' not in data.columns:
        print("Столбец 'Close' отсутствует в данных.")
        return

    if data.empty:
        print("Данные пусты.")
        return

    max_price = data['Close'].max()
    min_price = data['Close'].min()
    fluctuation = ((max_price - min_price) / min_price) * 100

    if fluctuation > threshold:
        print(f"Обнаружены сильные колебания цены акций: {fluctuation:.2f}% (порог: {threshold}%)")
    else:
        print(f"Колебания цены акций в пределах нормы: {fluctuation:.2f}% (порог: {threshold}%)")

def export_data_to_csv(data, filename):
    """
    Экспортирует данные об акциях в CSV файл в папку Data_CSV.

    :param data: DataFrame с данными о ценах акций.
    :param filename: Имя файла для сохранения данных.
    """
    # Имя папки для сохранения CSV файлов
    csv_folder = 'Data_CSV'

    # Проверка существования папки и создание её, если она не существует
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Полный путь к файлу
    full_path = os.path.join(csv_folder, filename)

    # Сохранение данных в CSV файл
    data.to_csv(full_path)

    # Вывод сообщения о том, что данные сохранены
    print(f"Данные успешно экспортированы в файл {full_path}")

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    # Создание файла styles.txt, если он не существует
    create_styles_file()

    # Ввод тикера акции и периода
    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца) или 'custom' для указания дат: ")

    if period.lower() == 'custom':
        start_date = input("Введите дату начала в формате YYYY-MM-DD: ")
        end_date = input("Введите дату окончания в формате YYYY-MM-DD: ")
    else:
        start_date = None
        end_date = None

    # Ввод порога колебаний
    threshold = float(input("Введите порог колебаний в процентах (например, '10' для 10%): "))

    # Уведомление о доступных стилях
    print("Доступные стили графиков можно посмотреть в файле 'styles.txt'.")

    # Ввод стиля графика
    style = input("Введите стиль графика (например, 'ggplot', 'seaborn-darkgrid', 'classic'): ")

    try:
        # Загрузка данных о акциях
        stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)

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
        dplt.create_and_save_plot(stock_data, ticker, period, style)

        # Экспорт данных в CSV файл
        csv_filename = f"{ticker}_{period}_stock_data.csv"
        export_data_to_csv(stock_data, csv_filename)

    except ValueError as ve:
        print(f"Ошибка ввода данных: {ve}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()