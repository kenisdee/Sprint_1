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
    fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12) = plt.subplots(12, 1, sharex=True, figsize=(14, 32))

    # Проверка наличия столбца 'Date' в данных
    if 'Date' not in data:
        # Если 'Date' отсутствует, проверяем индекс на тип datetime
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            ax1.plot(dates, data['Close'].values, label='Цена закрытия')
            ax1.plot(dates, data['Moving_Average'].values, label='Скользящее среднее', linestyle='--')
            ax1.plot(dates, data['Bollinger_Upper'].values, label='Верхняя полоса Боллинджера', linestyle='--', color='red')
            ax1.plot(dates, data['Bollinger_Lower'].values, label='Нижняя полоса Боллинджера', linestyle='--', color='green')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        # Если 'Date' присутствует, проверяем его на тип datetime
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        ax1.plot(data['Date'], data['Close'], label='Закрытие цены')
        ax1.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее', linestyle='--')
        ax1.plot(data['Date'], data['Bollinger_Upper'], label='Верхняя полоса Боллинджера', linestyle='--', color='red')
        ax1.plot(data['Date'], data['Bollinger_Lower'], label='Нижняя полоса Боллинджера', linestyle='--', color='green')

    # Настройка заголовка и меток осей для первого графика
    ax1.set_title(f"{ticker} Цена акций с течением времени")
    ax1.set_ylabel("Цена")
    ax1.legend()

    # График RSI
    ax2.plot(data.index, data['RSI'], label='RSI (Индекс относительной силы)', color='orange')
    ax2.set_title('RSI (Индекс относительной силы)')
    ax2.axhline(30, linestyle='--', alpha=0.5, color='red')
    ax2.axhline(70, linestyle='--', alpha=0.5, color='red')
    ax2.set_ylabel("RSI")
    ax2.legend()

    # График MACD
    ax3.plot(data.index, data['MACD'], label='MACD (Схождение — расхождение скользящих средних)', color='blue')
    ax3.plot(data.index, data['Signal'], label='Сигнал', color='red')
    ax3.set_title('MACD (Схождение — расхождение скользящих средних)')
    ax3.set_ylabel("MACD")
    ax3.legend()

    # График Stochastic Oscillator
    ax4.plot(data.index, data['Stochastic_K'], label='Stochastic %K (Быстрый стохастик)', color='purple')
    ax4.plot(data.index, data['Stochastic_D'], label='Stochastic %D (Медленный стохастик)', color='brown')
    ax4.set_title('Stochastic Oscillator (Стохастический Осциллятор)')
    ax4.set_ylabel("Stochastic")
    ax4.legend()

    # График OBV
    ax5.plot(data.index, data['OBV'], label='OBV (Индикатор балансового объема)', color='black')
    ax5.set_title('Индикатор балансового объема (OBV)')
    ax5.set_ylabel("OBV")
    ax5.legend()

    # График CCI
    ax6.plot(data.index, data['CCI'], label='CCI (Индекс товарного канала)', color='cyan')
    ax6.set_title('Индекс товарного канала (CCI)')
    ax6.set_ylabel("CCI")
    ax6.legend()

    # График MFI
    ax7.plot(data.index, data['MFI'], label='MFI (Индекс денежного потока)', color='magenta')
    ax7.set_title('Индекс денежного потока (MFI)')
    ax7.set_ylabel("MFI")
    ax7.legend()

    # График ADL
    ax8.plot(data.index, data['ADL'], label='ADL (Линия накопления/распределения)', color='yellow')
    ax8.set_title('Линия накопления/распределения (ADL)')
    ax8.set_ylabel("ADL")
    ax8.legend()

    # График Parabolic SAR
    ax9.plot(data.index, data['Parabolic_SAR'], label='Parabolic SAR (Параболическая система SAR)', color='green')
    ax9.set_title('Параболическая система SAR')
    ax9.set_xlabel("Дата")
    ax9.set_ylabel("Parabolic SAR")
    ax9.legend()

    # График Ichimoku Cloud
    ax10.plot(data.index, data['Ichimoku_Conversion'], label='Tenkan-sen (Тенкан-сен)', color='blue')
    ax10.plot(data.index, data['Ichimoku_Base'], label='Kijun-sen (Киджун-сен)', color='red')
    ax10.plot(data.index, data['Ichimoku_Leading_Span_A'], label='Senkou Span A (Сенкой спан A)', color='green', linestyle='--')
    ax10.plot(data.index, data['Ichimoku_Leading_Span_B'], label='Senkou Span B (Сенкой спан B)', color='purple', linestyle='--')
    ax10.plot(data.index, data['Ichimoku_Lagging_Span'], label='Chikou Span (Чикоу спан)', color='orange')
    ax10.fill_between(data.index, data['Ichimoku_Leading_Span_A'], data['Ichimoku_Leading_Span_B'], where=data['Ichimoku_Leading_Span_A'] >= data['Ichimoku_Leading_Span_B'], color='lightgreen', alpha=0.5)
    ax10.fill_between(data.index, data['Ichimoku_Leading_Span_A'], data['Ichimoku_Leading_Span_B'], where=data['Ichimoku_Leading_Span_A'] < data['Ichimoku_Leading_Span_B'], color='lightcoral', alpha=0.5)
    ax10.set_title('Ichimoku Cloud (Облако Ишимоку)')
    ax10.set_xlabel("Дата")
    ax10.set_ylabel("Цена")
    ax10.legend()

    # График VWAP
    ax11.plot(data.index, data['VWAP'], label='VWAP (Средневзвешенная по объему цена)', color='cyan')
    ax11.set_title('VWAP (Средневзвешенная по объему цена)')
    ax11.set_xlabel("Дата")
    ax11.set_ylabel("VWAP")
    ax11.legend()

    # График ATR
    ax12.plot(data.index, data['ATR'], label='ATR (Средний истинный диапазон)', color='magenta')
    ax12.set_title('ATR (Средний истинный диапазон)')
    ax12.set_xlabel("Дата")
    ax12.set_ylabel("ATR")
    ax12.legend()

    # Генерация имени файла, если оно не было предоставлено
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    # Сохранение графика в файл
    plt.tight_layout()
    plt.savefig(filename)
    print(f"График сохранен как {filename}")