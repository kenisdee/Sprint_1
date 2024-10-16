import logging
import os
import time
import unittest
from io import StringIO
from unittest.mock import patch

import pandas as pd

import data_download as dd
import data_plotting as dplt
from main import notify_if_strong_fluctuations, export_data_to_csv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Словарь для сопоставления имен тестов с их описаниями
test_descriptions = {
    'test_fetch_stock_data': 'Загрузка данных',
    'test_add_moving_average': 'Скользящее среднее',
    'test_calculate_and_display_average_price': 'Вычисление и вывод средней цены закрытия',
    'test_create_and_save_plot': 'Создание и сохранение графика',
    'test_notify_strong_fluctuations': 'Уведомление о сильных колебаниях',
    'test_notify_no_strong_fluctuations': 'Отсутствие уведомления о сильных колебаниях',
    'test_notify_missing_column': 'Отсутствие столбца "Close"',
    'test_notify_empty_data': 'Пустые данные',
    'test_export_data_to_csv': 'Экспорт данных в CSV файл'
}


class TestMain(unittest.TestCase):

    def setUp(self):
        # Логирование начала теста
        test_name = test_descriptions.get(self._testMethodName, self._testMethodName)
        logging.info(f"Начало теста: {test_name}")

    def tearDown(self):
        # Логирование завершения теста
        test_name = test_descriptions.get(self._testMethodName, self._testMethodName)
        logging.info(f"Завершение теста: {test_name}")

    def test_fetch_stock_data(self):
        """Тестирование загрузки данных."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        self.assertIsInstance(stock_data, pd.DataFrame)
        self.assertGreater(len(stock_data), 0)
        self.assertIn('Close', stock_data.columns)  # Проверка наличия столбца 'Close'
        logging.info("Данные успешно загружены.")

    def test_add_moving_average(self):
        """Тестирование добавления скользящего среднего."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stock_data_with_ma = dd.add_moving_average(stock_data)
        self.assertIn('Moving_Average', stock_data_with_ma.columns)
        logging.info("Скользящее среднее успешно добавлено.")

    @patch('sys.stdout', new_callable=StringIO)
    def test_calculate_and_display_average_price(self, mock_stdout):
        """Тестирование вычисления и вывода средней цены закрытия."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        dd.calculate_and_display_average_price(stock_data)
        # Проверка вывода
        expected_output = "Средняя цена закрытия акций: "
        self.assertIn(expected_output, mock_stdout.getvalue())
        # Проверка корректности вычисления средней цены закрытия
        average_price = stock_data['Close'].mean()
        self.assertAlmostEqual(float(mock_stdout.getvalue().split()[-1]), average_price, places=2)
        logging.info("Средняя цена закрытия успешно вычислена и отображена.")

    def test_create_and_save_plot(self):
        """Тестирование создания и сохранения графика."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stock_data = dd.add_moving_average(stock_data)
        self.assertIn('Moving_Average', stock_data.columns)  # Проверка наличия столбца 'Moving_Average'
        dplt.create_and_save_plot(stock_data, 'AAPL', '1mo')
        # Добавляем небольшую задержку, чтобы убедиться, что файл сохранен
        time.sleep(1)
        # Проверка на существование файла графика
        self.assertTrue(os.path.exists('AAPL_1mo_stock_price_chart.png'))
        # Очистка после теста
        os.remove('AAPL_1mo_stock_price_chart.png')
        logging.info("График успешно создан и сохранен.")

    @patch('builtins.print')
    def test_notify_strong_fluctuations(self, mock_print):
        """Тестирование уведомления о сильных колебаниях."""
        data = pd.DataFrame({
            'Close': [100, 105, 110, 108, 115, 120, 118, 125, 130, 128]
        })
        notify_if_strong_fluctuations(data, 10)
        mock_print.assert_called_with("Обнаружены сильные колебания цены акций: 30.00% (порог: 10%)")
        logging.info("Уведомление о сильных колебаниях успешно проверено.")

    @patch('builtins.print')
    def test_notify_no_strong_fluctuations(self, mock_print):
        """Тестирование отсутствия уведомления о сильных колебаниях."""
        data = pd.DataFrame({
            'Close': [100, 105, 110, 108, 115, 120, 118, 125, 130, 128]
        })
        notify_if_strong_fluctuations(data, 30)
        mock_print.assert_called_with("Колебания цены акций в пределах нормы: 30.00% (порог: 30%)")
        logging.info("Уведомление об отсутствии сильных колебаний успешно проверено.")

    @patch('builtins.print')
    def test_notify_missing_column(self, mock_print):
        """Тестирование отсутствия столбца 'Close'."""
        notify_if_strong_fluctuations(pd.DataFrame(), 10)
        mock_print.assert_called_with("Столбец 'Close' отсутствует в данных.")
        logging.info("Тест на отсутствие столбца 'Close' успешно пройден.")

    @patch('builtins.print')
    def test_notify_empty_data(self, mock_print):
        """Тестирование пустых данных."""
        notify_if_strong_fluctuations(pd.DataFrame({'Close': []}), 10)
        mock_print.assert_called_with("Данные пусты.")
        logging.info("Тест на пустые данные успешно пройден.")

    def test_export_data_to_csv(self):
        """Тестирование экспорта данных в CSV файл."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        csv_filename = 'test_export_data.csv'
        export_data_to_csv(stock_data, csv_filename)
        # Проверка на существование файла
        self.assertTrue(os.path.exists(csv_filename))
        # Загрузка данных из CSV файла для проверки
        loaded_data = pd.read_csv(csv_filename)
        self.assertEqual(len(stock_data), len(loaded_data))
        # Очистка после теста
        os.remove(csv_filename)
        logging.info("Данные успешно экспортированы и проверены.")


if __name__ == "__main__":
    unittest.main()
