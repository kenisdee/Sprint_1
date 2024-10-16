import unittest
import data_download as dd
import data_plotting as dplt
import pandas as pd
import os
import time
from io import StringIO
import sys
from unittest.mock import patch

class TestMain(unittest.TestCase):

    def test_fetch_stock_data(self):
        # Тестирование загрузки данных
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        self.assertIsInstance(stock_data, pd.DataFrame)
        self.assertGreater(len(stock_data), 0)

    def test_add_moving_average(self):
        # Тестирование добавления скользящего среднего
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stock_data_with_ma = dd.add_moving_average(stock_data)
        self.assertIn('Moving_Average', stock_data_with_ma.columns)

    @patch('sys.stdout', new_callable=StringIO)
    def test_calculate_and_display_average_price(self, mock_stdout):
        # Тестирование вычисления и вывода средней цены закрытия
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        dd.calculate_and_display_average_price(stock_data)
        # Проверка вывода
        expected_output = "Средняя цена закрытия акций: "
        self.assertIn(expected_output, mock_stdout.getvalue())

    def test_create_and_save_plot(self):
        # Тестирование создания и сохранения графика
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stock_data = dd.add_moving_average(stock_data)  # Убедитесь, что столбец добавлен
        dplt.create_and_save_plot(stock_data, 'AAPL', '1mo')
        # Добавляем небольшую задержку, чтобы убедиться, что файл сохранен
        time.sleep(1)
        # Проверка на существование файла графика
        self.assertTrue(os.path.exists('AAPL_1mo_stock_price_chart.png'))
        # Очистка после теста
        os.remove('AAPL_1mo_stock_price_chart.png')

if __name__ == "__main__":
    unittest.main()