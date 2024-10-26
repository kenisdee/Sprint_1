import os
import matplotlib.pyplot as plt
import pandas as pd


def plot_price_and_moving_average(ax, data):
    """Построение графика цены закрытия и скользящего среднего."""
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            ax.plot(dates, data['Close'].values, label='Цена закрытия')
            ax.plot(dates, data['Moving_Average'].values, label='Скользящее среднее', linestyle='--')
            ax.plot(dates, data['Bollinger_Upper'].values, label='Верхняя полоса Боллинджера', linestyle='--',
                    color='red')
            ax.plot(dates, data['Bollinger_Lower'].values, label='Нижняя полоса Боллинджера', linestyle='--',
                    color='green')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        ax.plot(data['Date'], data['Close'], label='Закрытие цены')
        ax.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее', linestyle='--')
        ax.plot(data['Date'], data['Bollinger_Upper'], label='Верхняя полоса Боллинджера', linestyle='--', color='red')
        ax.plot(data['Date'], data['Bollinger_Lower'], label='Нижняя полоса Боллинджера', linestyle='--', color='green')
    ax.set_ylabel("Цена")
    ax.legend()


def plot_rsi(ax, data):
    """Построение графика RSI."""
    ax.plot(data.index, data['RSI'], label='RSI (Индекс относительной силы)', color='orange')
    ax.axhline(30, linestyle='--', alpha=0.5, color='red')
    ax.axhline(70, linestyle='--', alpha=0.5, color='red')
    ax.set_ylabel("RSI")
    ax.legend()


def plot_macd(ax, data):
    """Построение графика MACD."""
    ax.plot(data.index, data['MACD'], label='MACD (Схождение — расхождение скользящих средних)', color='blue')
    ax.plot(data.index, data['Signal'], label='Сигнал', color='red')
    ax.set_ylabel("MACD")
    ax.legend()


def plot_stochastic_oscillator(ax, data):
    """Построение графика Stochastic Oscillator."""
    ax.plot(data.index, data['Stochastic_K'], label='Stochastic %K (Быстрый стохастик)', color='purple')
    ax.plot(data.index, data['Stochastic_D'], label='Stochastic %D (Медленный стохастик)', color='brown')
    ax.set_ylabel("Stochastic")
    ax.legend()


def plot_obv(ax, data):
    """Построение графика OBV."""
    ax.plot(data.index, data['OBV'], label='OBV (Индикатор балансового объема)', color='black')
    ax.set_ylabel("OBV")
    ax.legend()


def plot_cci(ax, data):
    """Построение графика CCI."""
    ax.plot(data.index, data['CCI'], label='CCI (Индекс товарного канала)', color='cyan')
    ax.set_ylabel("CCI")
    ax.legend()


def plot_mfi(ax, data):
    """Построение графика MFI."""
    ax.plot(data.index, data['MFI'], label='MFI (Индекс денежного потока)', color='magenta')
    ax.set_ylabel("MFI")
    ax.legend()


def plot_adl(ax, data):
    """Построение графика ADL."""
    ax.plot(data.index, data['ADL'], label='ADL (Линия накопления/распределения)', color='yellow')
    ax.set_ylabel("ADL")
    ax.legend()


def plot_parabolic_sar(ax, data):
    """Построение графика Parabolic SAR."""
    ax.plot(data.index, data['Parabolic_SAR'], label='Parabolic SAR (Параболическая система SAR)', color='green')
    ax.set_ylabel("Parabolic SAR")
    ax.legend()


def plot_ichimoku_cloud(ax, data):
    """Построение графика Ichimoku Cloud."""
    ax.plot(data.index, data['Ichimoku_Conversion'], label='Tenkan-sen (Быстрая линия, линия переворота)', color='blue')
    ax.plot(data.index, data['Ichimoku_Base'], label='Kijun-sen (Медленная линия, линия стандарта)', color='red')
    ax.plot(data.index, data['Ichimoku_Leading_Span_A'], label='Senkou Span A (Первая ведущая линия, SSA)',
            color='green', linestyle='--')
    ax.plot(data.index, data['Ichimoku_Leading_Span_B'], label='Senkou Span B (Вторая ведущая линия, SSB)',
            color='purple', linestyle='--')
    ax.plot(data.index, data['Ichimoku_Lagging_Span'], label='Chikou Span (Запаздывающая линия)', color='orange')
    ax.fill_between(data.index, data['Ichimoku_Leading_Span_A'], data['Ichimoku_Leading_Span_B'],
                    where=data['Ichimoku_Leading_Span_A'] >= data['Ichimoku_Leading_Span_B'], color='lightgreen',
                    alpha=0.5)
    ax.fill_between(data.index, data['Ichimoku_Leading_Span_A'], data['Ichimoku_Leading_Span_B'],
                    where=data['Ichimoku_Leading_Span_A'] < data['Ichimoku_Leading_Span_B'], color='lightcoral',
                    alpha=0.5)
    ax.set_ylabel("Цена")
    ax.legend()


def plot_vwap(ax, data):
    """Построение графика VWAP."""
    ax.plot(data.index, data['VWAP'], label='VWAP (Средневзвешенная по объему цена)', color='cyan')
    ax.set_ylabel("VWAP")
    ax.legend()


def plot_atr(ax, data):
    """Построение графика ATR."""
    ax.plot(data.index, data['ATR'], label='ATR (Средний истинный диапазон)', color='magenta')
    ax.set_ylabel("ATR")
    ax.legend()


def plot_std_deviation(ax, data):
    """Построение графика стандартного отклонения цены закрытия."""
    ax.plot(data.index, data['Std_Deviation'], label='Стандартное отклонение', color='purple')
    ax.set_ylabel("Стандартное отклонение")
    ax.legend()


def plot_mean_closing_price(ax, data):
    """Построение графика среднего значения цены закрытия."""
    mean_closing_price = data['Mean_Closing_Price'].iloc[0]
    ax.axhline(mean_closing_price, label='Среднее значение цены закрытия', color='blue', linestyle='--')
    x_mid = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    ax.text(x_mid, mean_closing_price, f'{mean_closing_price:.2f}', verticalalignment='bottom', horizontalalignment='center')
    ax.set_ylabel("Цена")
    ax.legend()


def plot_variance_closing_price(ax, data):
    """Построение графика дисперсии цены закрытия."""
    variance_closing_price = data['Variance_Closing_Price'].iloc[0]
    ax.axhline(variance_closing_price, label='Дисперсия цены закрытия', color='green', linestyle='--')
    x_mid = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    ax.text(x_mid, variance_closing_price, f'{variance_closing_price:.2f}', verticalalignment='bottom', horizontalalignment='center')
    ax.set_ylabel("Дисперсия")
    ax.legend()


def plot_coefficient_of_variation(ax, data):
    """Построение графика коэффициента вариации."""
    coefficient_of_variation = data['Coefficient_of_Variation'].iloc[0]
    ax.axhline(coefficient_of_variation, label='Коэффициент вариации', color='red', linestyle='--')
    x_mid = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
    ax.text(x_mid, coefficient_of_variation, f'{coefficient_of_variation:.2f}%', verticalalignment='bottom', horizontalalignment='center')
    ax.set_ylabel("Коэффициент вариации (%)")
    ax.legend()


def create_and_save_plot(data, ticker, period, style='classic', filename=None):
    """
    Создает и сохраняет график цены акций с течением времени.

    :param data: DataFrame с данными о ценах закрытия и скользящем среднем.
    :param ticker: Тикер акции.
    :param period: Период данных.
    :param style: Стиль графика (по умолчанию 'classic').
    :param filename: Имя файла для сохранения графика (по умолчанию генерируется автоматически).
    """
    # Проверка на пустые данные
    if data.empty:
        raise ValueError("Данные пусты.")

    # Имя папки для сохранения графиков
    chart_folder = 'Chart'

    # Проверка существования папки и создание её, если она не существует
    if not os.path.exists(chart_folder):
        os.makedirs(chart_folder)

    # Применение выбранного стиля
    if style in plt.style.available:
        plt.style.use(style)
    else:
        print(f"Стиль '{style}' не найден. Используется стиль по умолчанию.")
        plt.style.use('classic')

    # Создание фигуры для графика
    fig, axes = plt.subplots(16, 1, sharex=True, figsize=(14, 48))

    # Проверка наличия необходимых столбцов
    required_columns = ['Close', 'Moving_Average', 'Bollinger_Upper', 'Bollinger_Lower', 'RSI', 'MACD', 'Signal',
                        'Stochastic_K', 'Stochastic_D', 'OBV', 'CCI', 'MFI', 'ADL', 'Parabolic_SAR',
                        'Ichimoku_Conversion', 'Ichimoku_Base', 'Ichimoku_Leading_Span_A', 'Ichimoku_Leading_Span_B',
                        'Ichimoku_Lagging_Span', 'VWAP', 'ATR', 'Std_Deviation', 'Mean_Closing_Price',
                        'Variance_Closing_Price', 'Coefficient_of_Variation']
    for column in required_columns:
        if column not in data.columns:
            print(f"Столбец '{column}' отсутствует в данных.")
            return

    # Построение графиков
    plot_price_and_moving_average(axes[0], data)
    axes[0].set_title(f"{ticker} Цена акций с течением времени")

    plot_rsi(axes[1], data)
    axes[1].set_title('RSI (Индекс относительной силы)')

    plot_macd(axes[2], data)
    axes[2].set_title('MACD (Схождение — расхождение скользящих средних)')

    plot_stochastic_oscillator(axes[3], data)
    axes[3].set_title('Stochastic Oscillator (Стохастический Осциллятор)')

    plot_obv(axes[4], data)
    axes[4].set_title('Индикатор балансового объема (OBV)')

    plot_cci(axes[5], data)
    axes[5].set_title('Индекс товарного канала (CCI)')

    plot_mfi(axes[6], data)
    axes[6].set_title('Индекс денежного потока (MFI)')

    plot_adl(axes[7], data)
    axes[7].set_title('Линия накопления/распределения (ADL)')

    plot_parabolic_sar(axes[8], data)
    axes[8].set_title('Параболическая система SAR')
    axes[8].set_xlabel("Дата")

    plot_ichimoku_cloud(axes[9], data)
    axes[9].set_title('Ichimoku Cloud (Облако Ишимоку)')
    axes[9].set_xlabel("Дата")

    plot_vwap(axes[10], data)
    axes[10].set_title('VWAP (Средневзвешенная по объему цена)')
    axes[10].set_xlabel("Дата")

    plot_atr(axes[11], data)
    axes[11].set_title('ATR (Средний истинный диапазон)')
    axes[11].set_xlabel("Дата")

    plot_std_deviation(axes[12], data)
    axes[12].set_title('Стандартное отклонение цены закрытия')
    axes[12].set_xlabel("Дата")

    plot_mean_closing_price(axes[13], data)
    axes[13].set_title('Среднее значение цены закрытия')
    axes[13].set_xlabel("Дата")

    plot_variance_closing_price(axes[14], data)
    axes[14].set_title('Дисперсия цены закрытия')
    axes[14].set_xlabel("Дата")

    plot_coefficient_of_variation(axes[15], data)
    axes[15].set_title('Коэффициент вариации')
    axes[15].set_xlabel("Дата")

    # Генерация имени файла, если оно не было предоставлено
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    # Полный путь к файлу
    full_path = os.path.join(chart_folder, filename)

    # Сохранение графика в файл
    plt.tight_layout()
    plt.savefig(full_path)
    print(f"График сохранен как {full_path}")