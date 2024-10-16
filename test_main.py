import os
import time
import unittest
from io import StringIO
from unittest.mock import patch
import logging

import pandas as pd

import data_download as dd
import data_plotting as dplt

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestMain(unittest.TestCase):

    def setUp(self):
        # Логирование начала теста
        logging.info(f"Начало теста: {self._testMethodName}")

    def tearDown(self):
        # Логирование завершения теста
        logging.info(f"Завершение теста: {self._testMethodName}")

    def test_fetch_stock_data(self):
        # Тестирование загрузки данных
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        self.assertIsInstance(stock_data, pd.DataFrame)
        self.assertGreater(len(stock_data), 0)
        self.assertIn('Close', stock_data.columns)  # Проверка наличия столбца 'Close'
        logging.info("Данные успешно загружены.")

    def test_add_moving_average(self):
        # Тестирование добавления скользящего среднего
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stock_data_with_ma = dd.add_moving_average(stock_data)
        self.assertIn('Moving_Average', stock_data_with_ma.columns)
        logging.info("Скользящее среднее успешно добавлено.")

    @patch('sys.stdout', new_callable=StringIO)
    def test_calculate_and_display_average_price(self, mock_stdout):
        # Тестирование вычисления и вывода средней цены закрытия
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
        # Тестирование создания и сохранения графика
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stock_data = dd.add_moving_average(stock_data)  # Убедитесь, что столбец добавлен
        self.assertIn('Moving_Average', stock_data.columns)  # Проверка наличия столбца 'Moving_Average'
        dplt.create_and_save_plot(stock_data, 'AAPL', '1mo')
        # Добавляем небольшую задержку, чтобы убедиться, что файл сохранен
        time.sleep(1)
        # Проверка на существование файла графика
        self.assertTrue(os.path.exists('AAPL_1mo_stock_price_chart.png'))
        # Очистка после теста
        os.remove('AAPL_1mo_stock_price_chart.png')
        logging.info("График успешно создан и сохранен.")

if __name__ == "__main__":
    unittest.main()