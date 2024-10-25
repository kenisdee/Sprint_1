import logging
import os
import time
import unittest
from io import StringIO
from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd

import data_download as dd
import data_plotting as dplt
from main import notify_if_strong_fluctuations, export_data_to_csv, create_styles_file

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создание папки для логов, если она не существует
log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Добавление обработчика для записи логов в файл
log_filename = os.path.join(log_folder, 'test_log.log')
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

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
    'test_export_data_to_csv': 'Экспорт данных в CSV файл',
    'test_calculate_rsi': 'Расчет RSI',
    'test_calculate_macd': 'Расчет MACD',
    'test_calculate_bollinger_bands': 'Расчет Bollinger Bands',
    'test_calculate_stochastic_oscillator': 'Расчет Stochastic Oscillator',
    'test_calculate_vwap': 'Расчет VWAP',
    'test_calculate_atr': 'Расчет ATR',
    'test_calculate_obv': 'Расчет OBV',
    'test_calculate_cci': 'Расчет CCI',
    'test_calculate_mfi': 'Расчет MFI',
    'test_calculate_adl': 'Расчет ADL',
    'test_calculate_parabolic_sar': 'Расчет Parabolic SAR',
    'test_calculate_ichimoku_cloud': 'Расчет Ichimoku Cloud',
    'test_create_styles_file': 'Создание файла стилей'
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
        # Проверка на существование файла графика в папке Price_chart
        chart_filename = 'AAPL_1mo_stock_price_chart.png'
        full_path = os.path.join('Chart', chart_filename)
        self.assertTrue(os.path.exists(full_path))
        # Очистка после теста
        os.remove(full_path)
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
        # Проверка на существование файла в папке CSV
        full_path = os.path.join('Data_CSV', csv_filename)
        self.assertTrue(os.path.exists(full_path))
        # Загрузка данных из CSV файла для проверки
        loaded_data = pd.read_csv(full_path)
        self.assertEqual(len(stock_data), len(loaded_data))
        # Очистка после теста
        os.remove(full_path)
        logging.info("Данные успешно экспортированы и проверены.")

    def test_calculate_rsi(self):
        """Тестирование расчета RSI."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        rsi = dd.calculate_rsi(stock_data)
        self.assertIn('RSI', stock_data.columns)
        self.assertIsInstance(rsi, pd.Series)
        logging.info("RSI успешно рассчитан.")

    def test_calculate_macd(self):
        """Тестирование расчета MACD."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        macd, signal = dd.calculate_macd(stock_data)
        self.assertIn('MACD', stock_data.columns)
        self.assertIn('Signal', stock_data.columns)
        self.assertIsInstance(macd, pd.Series)
        self.assertIsInstance(signal, pd.Series)
        logging.info("MACD успешно рассчитан.")

    def test_calculate_bollinger_bands(self):
        """Тестирование расчета Bollinger Bands."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        upper_band, middle_band, lower_band = dd.calculate_bollinger_bands(stock_data)
        self.assertIn('Bollinger_Upper', stock_data.columns)
        self.assertIn('Bollinger_Middle', stock_data.columns)
        self.assertIn('Bollinger_Lower', stock_data.columns)
        self.assertIsInstance(upper_band, pd.Series)
        self.assertIsInstance(middle_band, pd.Series)
        self.assertIsInstance(lower_band, pd.Series)
        logging.info("Bollinger Bands успешно рассчитаны.")

    def test_calculate_stochastic_oscillator(self):
        """Тестирование расчета Stochastic Oscillator."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        stochastic_k, stochastic_d = dd.calculate_stochastic_oscillator(stock_data)
        self.assertIn('Stochastic_K', stock_data.columns)
        self.assertIn('Stochastic_D', stock_data.columns)
        self.assertIsInstance(stochastic_k, pd.Series)
        self.assertIsInstance(stochastic_d, pd.Series)
        logging.info("Stochastic Oscillator успешно рассчитан.")

    def test_calculate_vwap(self):
        """Тестирование расчета VWAP."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        vwap = dd.calculate_vwap(stock_data)
        self.assertIn('VWAP', stock_data.columns)
        self.assertIsInstance(vwap, pd.Series)
        logging.info("VWAP успешно рассчитан.")

    def test_calculate_atr(self):
        """Тестирование расчета ATR."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        atr = dd.calculate_atr(stock_data)
        self.assertIn('ATR', stock_data.columns)
        self.assertIsInstance(atr, pd.Series)
        logging.info("ATR успешно рассчитан.")

    def test_calculate_obv(self):
        """Тестирование расчета OBV."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        obv = dd.calculate_obv(stock_data)
        self.assertIn('OBV', stock_data.columns)
        self.assertIsInstance(obv, pd.Series)
        logging.info("OBV успешно рассчитан.")

    def test_calculate_cci(self):
        """Тестирование расчета CCI."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        cci = dd.calculate_cci(stock_data)
        self.assertIn('CCI', stock_data.columns)
        self.assertIsInstance(cci, pd.Series)
        logging.info("CCI успешно рассчитан.")

    def test_calculate_mfi(self):
        """Тестирование расчета MFI."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        mfi = dd.calculate_mfi(stock_data)
        self.assertIn('MFI', stock_data.columns)
        self.assertIsInstance(mfi, pd.Series)
        logging.info("MFI успешно рассчитан.")

    def test_calculate_adl(self):
        """Тестирование расчета ADL."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        adl = dd.calculate_adl(stock_data)
        self.assertIn('ADL', stock_data.columns)
        self.assertIsInstance(adl, pd.Series)
        logging.info("ADL успешно рассчитан.")

    def test_calculate_parabolic_sar(self):
        """Тестирование расчета Parabolic SAR."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        parabolic_sar = dd.calculate_parabolic_sar(stock_data)
        self.assertIn('Parabolic_SAR', stock_data.columns)
        self.assertIsInstance(parabolic_sar, pd.Series)
        logging.info("Parabolic SAR успешно рассчитан.")

    def test_calculate_ichimoku_cloud(self):
        """Тестирование расчета Ichimoku Cloud."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        ichimoku_cloud = dd.calculate_ichimoku_cloud(stock_data)
        self.assertIn('Ichimoku_Conversion', stock_data.columns)
        self.assertIn('Ichimoku_Base', stock_data.columns)
        self.assertIn('Ichimoku_Leading_Span_A', stock_data.columns)
        self.assertIn('Ichimoku_Leading_Span_B', stock_data.columns)
        self.assertIn('Ichimoku_Lagging_Span', stock_data.columns)
        self.assertIsInstance(ichimoku_cloud, tuple)
        logging.info("Ichimoku Cloud успешно рассчитан.")

    def test_create_styles_file(self):
        """Тестирование создания файла стилей."""
        create_styles_file()
        styles_file = 'styles.txt'
        self.assertTrue(os.path.exists(styles_file))
        with open(styles_file, 'r') as file:
            styles = file.readlines()
        self.assertGreater(len(styles), 0)
        os.remove(styles_file)
        logging.info("Файл стилей успешно создан и проверен.")

    # Тестирование построения графиков:

    def test_plot_price_and_moving_average(self):
        """Тестирование построения графика цены закрытия и скользящего среднего."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_price_and_moving_average(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График цены закрытия и скользящего среднего успешно построен.")

    def test_plot_rsi(self):
        """Тестирование построения графика RSI."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_rsi(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График RSI успешно построен.")

    def test_plot_macd(self):
        """Тестирование построения графика MACD."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_macd(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График MACD успешно построен.")

    def test_plot_stochastic_oscillator(self):
        """Тестирование построения графика Stochastic Oscillator."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_stochastic_oscillator(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График Stochastic Oscillator успешно построен.")

    def test_plot_obv(self):
        """Тестирование построения графика OBV."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_obv(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График OBV успешно построен.")

    def test_plot_cci(self):
        """Тестирование построения графика CCI."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_cci(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График CCI успешно построен.")

    def test_plot_mfi(self):
        """Тестирование построения графика MFI."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_mfi(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График MFI успешно построен.")

    def test_plot_adl(self):
        """Тестирование построения графика ADL."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_adl(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График ADL успешно построен.")

    def test_plot_parabolic_sar(self):
        """Тестирование построения графика Parabolic SAR."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_parabolic_sar(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График Parabolic SAR успешно построен.")

    def test_plot_ichimoku_cloud(self):
        """Тестирование построения графика Ichimoku Cloud."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_ichimoku_cloud(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График Ichimoku Cloud успешно построен.")

    def test_plot_vwap(self):
        """Тестирование построения графика VWAP."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_vwap(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График VWAP успешно построен.")

    def test_plot_atr(self):
        """Тестирование построения графика ATR."""
        stock_data = dd.fetch_stock_data('AAPL', '1mo')
        fig, ax = plt.subplots()
        dplt.plot_atr(ax, stock_data)
        self.assertIsNotNone(ax.get_legend())
        logging.info("График ATR успешно построен.")


if __name__ == "__main__":
    unittest.main()
