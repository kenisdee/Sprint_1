# Проект анализа и визуализации данных о ценах акций

Этот проект предназначен для загрузки, анализа и визуализации исторических данных о ценах акций с использованием
библиотеки `yfinance`. Проект также включает в себя расчет различных технических индикаторов и сохранение результатов в
формате CSV.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [Функции](#функции)
- [Контакты](#контакты)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/kenisdee/Sprint_1.git

2. Перейдите в директорию проекта:

   ```bash
   cd Sprint_1

3. Создайте виртуальное окружение:

   ```bash
   python3 -m venv venv

4. Активируйте виртуальное окружение:

   ```bash
   source venv/bin/activate

5. Установите зависимости:

   ```bash
   pip3 install -r requirements.txt

## Использование

1. Запуск проекта:

   ```bash
   python3 main.py

После выполнения создаются и сохраняются графики в виде изображения и данные в формате CSV.

2. Запуск тестирования:

   ```bash
   python3 test_main.py

Тесты проверяют корректность работы всех функций и сохраняют логи в файл test_log.log.

## Функции

| Функция                                                                                                    | Описание                                            |
|------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| fetch_stock_data(ticker, period)                                                                           | Загружает исторические данные о ценах акций         |
| calculate_rsi(data, period)                                                                                | Рассчитывает индекс относительной силы (RSI)        |
| calculate_macd(data, short_period, long_period, signal_period)                                             | Рассчитывает индикатор MACD                         |
| calculate_bollinger_bands(data, window, num_std)                                                           | Рассчитывает линии Боллинджера                      |
| calculate_stochastic_oscillator(data, k_period, d_period)                                                  | Рассчитывает стохастический осциллятор              |
| calculate_vwap(data)                                                                                       | Рассчитывает средневзвешенную по объему цену (VWAP) |
| calculate_atr(data, period)                                                                                | Рассчитывает средний истинный диапазон (ATR)        |
| calculate_obv(data)                                                                                        | Рассчитывает накопленный объем (OBV)                |
| calculate_cci(data, period)                                                                                | Рассчитывает индекс товарного канала (CCI)          |
| calculate_mfi(data, period)                                                                                | Рассчитывает индекс денежного потока (MFI)          |
| calculate_adl(data)                                                                                        | Рассчитывает накопленный объем (ADL)                |
| calculate_parabolic_sar(data, acceleration, max_acceleration)                                              | Рассчитывает параболический SAR                     |
| calculate_ichimoku_cloud(data, conversion_period, base_period, leading_span_b_period, lagging_span_period) | Рассчитывает облако Ишимоку                         |
| create_and_save_plot(data, ticker, period)                                                                 | Создает и сохраняет график цен акций                |
| export_data_to_csv(data, filename)                                                                         | Экспортирует данные в CSV файл                      |

## Контакты

Для связи с автором проекта, пожалуйста, используйте следующие контактные данные:

Email: kenisdee@ya.ru

GitHub: https://github.com/kenisdee