import os

import plotly.graph_objs as go
import plotly.subplots as sp


def plot_price_and_moving_average(data):
    """Построение интерактивного графика цены закрытия и скользящего среднего."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Цена закрытия'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Скользящее среднее',
                             line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=data['Bollinger_Upper'], mode='lines', name='Верхняя полоса Боллинджера',
                             line=dict(dash='dash', color='red')))
    fig.add_trace(go.Scatter(x=data.index, y=data['Bollinger_Lower'], mode='lines', name='Нижняя полоса Боллинджера',
                             line=dict(dash='dash', color='green')))

    fig.update_layout(title='Цена закрытия и скользящее среднее', xaxis_title='Дата', yaxis_title='Цена')
    return fig


def plot_rsi(data):
    """Построение интерактивного графика RSI."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    fig.add_shape(type="line", x0=data.index[0], x1=data.index[-1], y0=30, y1=30, line=dict(color="red", dash="dash"))
    fig.add_shape(type="line", x0=data.index[0], x1=data.index[-1], y0=70, y1=70, line=dict(color="red", dash="dash"))

    fig.update_layout(title='RSI (Индекс относительной силы)', xaxis_title='Дата', yaxis_title='RSI')
    return fig


def plot_macd(data):
    """Построение интерактивного графика MACD."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Signal'], mode='lines', name='Сигнал', line=dict(color='red')))

    fig.update_layout(title='MACD (Схождение — расхождение скользящих средних)', xaxis_title='Дата', yaxis_title='MACD')
    return fig


def plot_stochastic_oscillator(data):
    """Построение интерактивного графика Stochastic Oscillator."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Stochastic_K'], mode='lines', name='Stochastic %K'))
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Stochastic_D'], mode='lines', name='Stochastic %D', line=dict(color='red')))

    fig.update_layout(title='Stochastic Oscillator (Стохастический Осциллятор)', xaxis_title='Дата',
                      yaxis_title='Stochastic')
    return fig


def plot_obv(data):
    """Построение интерактивного графика OBV."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['OBV'], mode='lines', name='OBV'))

    fig.update_layout(title='Индикатор балансового объема (OBV)', xaxis_title='Дата', yaxis_title='OBV')
    return fig


def plot_cci(data):
    """Построение интерактивного графика CCI."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['CCI'], mode='lines', name='CCI'))

    fig.update_layout(title='Индекс товарного канала (CCI)', xaxis_title='Дата', yaxis_title='CCI')
    return fig


def plot_mfi(data):
    """Построение интерактивного графика MFI."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['MFI'], mode='lines', name='MFI'))

    fig.update_layout(title='Индекс денежного потока (MFI)', xaxis_title='Дата', yaxis_title='MFI')
    return fig


def plot_adl(data):
    """Построение интерактивного графика ADL."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['ADL'], mode='lines', name='ADL'))

    fig.update_layout(title='Линия накопления/распределения (ADL)', xaxis_title='Дата', yaxis_title='ADL')
    return fig


def plot_parabolic_sar(data):
    """Построение интерактивного графика Parabolic SAR."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Parabolic_SAR'], mode='lines', name='Parabolic SAR'))

    fig.update_layout(title='Параболическая система SAR', xaxis_title='Дата', yaxis_title='Parabolic SAR')
    return fig


def plot_ichimoku_cloud(data):
    """Построение интерактивного графика Ichimoku Cloud."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Ichimoku_Conversion'], mode='lines',
                             name='Tenkan-sen (Быстрая линия, линия переворота)'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Ichimoku_Base'], mode='lines',
                             name='Kijun-sen (Медленная линия, линия стандарта)'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Ichimoku_Leading_Span_A'], mode='lines',
                             name='Senkou Span A (Первая ведущая линия, SSA)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=data['Ichimoku_Leading_Span_B'], mode='lines',
                             name='Senkou Span B (Вторая ведущая линия, SSB)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=data['Ichimoku_Lagging_Span'], mode='lines',
                             name='Chikou Span (Запаздывающая линия)'))

    fig.update_layout(title='Ichimoku Cloud (Облако Ишимоку)', xaxis_title='Дата', yaxis_title='Цена')
    return fig


def plot_vwap(data):
    """Построение интерактивного графика VWAP."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], mode='lines', name='VWAP'))

    fig.update_layout(title='VWAP (Средневзвешенная по объему цена)', xaxis_title='Дата', yaxis_title='VWAP')
    return fig


def plot_atr(data):
    """Построение интерактивного графика ATR."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['ATR'], mode='lines', name='ATR'))

    fig.update_layout(title='ATR (Средний истинный диапазон)', xaxis_title='Дата', yaxis_title='ATR')
    return fig


def plot_std_deviation(data):
    """Построение интерактивного графика стандартного отклонения цены закрытия."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Std_Deviation'], mode='lines', name='Стандартное отклонение'))

    fig.update_layout(title='Стандартное отклонение цены закрытия', xaxis_title='Дата',
                      yaxis_title='Стандартное отклонение')
    return fig


def plot_mean_closing_price(data):
    """Построение интерактивного графика среднего значения цены закрытия."""
    fig = go.Figure()

    mean_closing_price = data['Mean_Closing_Price'].iloc[0]
    fig.add_trace(go.Scatter(x=data.index, y=[mean_closing_price] * len(data), mode='lines',
                             name='Среднее значение цены закрытия', line=dict(dash='dash')))

    fig.update_layout(title='Среднее значение цены закрытия', xaxis_title='Дата', yaxis_title='Цена')
    return fig


def plot_variance_closing_price(data):
    """Построение интерактивного графика дисперсии цены закрытия."""
    fig = go.Figure()

    variance_closing_price = data['Variance_Closing_Price'].iloc[0]
    fig.add_trace(
        go.Scatter(x=data.index, y=[variance_closing_price] * len(data), mode='lines', name='Дисперсия цены закрытия',
                   line=dict(dash='dash')))

    fig.update_layout(title='Дисперсия цены закрытия', xaxis_title='Дата', yaxis_title='Дисперсия')
    return fig


def plot_coefficient_of_variation(data):
    """Построение интерактивного графика коэффициента вариации."""
    fig = go.Figure()

    coefficient_of_variation = data['Coefficient_of_Variation'].iloc[0]
    fig.add_trace(
        go.Scatter(x=data.index, y=[coefficient_of_variation] * len(data), mode='lines', name='Коэффициент вариации',
                   line=dict(dash='dash')))

    fig.update_layout(title='Коэффициент вариации', xaxis_title='Дата', yaxis_title='Коэффициент вариации (%)')
    return fig


def create_and_save_plot(data, ticker, period, filename=None):
    """Создание и сохранение интерактивного графика."""
    # Проверка на пустые данные
    if data.empty:
        raise ValueError("Данные пусты.")

    # Имя папки для сохранения графиков
    chart_folder = 'Chart'

    # Проверка существования папки и создание её, если она не существует
    if not os.path.exists(chart_folder):
        os.makedirs(chart_folder)

    # Генерация имени файла, если оно не было предоставлено
    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.html"

    # Полный путь к файлу
    full_path = os.path.join(chart_folder, filename)

    # Создание подграфиков
    fig = sp.make_subplots(rows=16, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Построение графиков
    fig.add_trace(plot_price_and_moving_average(data).data[0], row=1, col=1)
    fig.add_trace(plot_price_and_moving_average(data).data[1], row=1, col=1)
    fig.add_trace(plot_price_and_moving_average(data).data[2], row=1, col=1)
    fig.add_trace(plot_price_and_moving_average(data).data[3], row=1, col=1)

    fig.add_trace(plot_rsi(data).data[0], row=2, col=1)

    fig.add_trace(plot_macd(data).data[0], row=3, col=1)
    fig.add_trace(plot_macd(data).data[1], row=3, col=1)

    fig.add_trace(plot_stochastic_oscillator(data).data[0], row=4, col=1)
    fig.add_trace(plot_stochastic_oscillator(data).data[1], row=4, col=1)

    fig.add_trace(plot_obv(data).data[0], row=5, col=1)

    fig.add_trace(plot_cci(data).data[0], row=6, col=1)

    fig.add_trace(plot_mfi(data).data[0], row=7, col=1)

    fig.add_trace(plot_adl(data).data[0], row=8, col=1)

    fig.add_trace(plot_parabolic_sar(data).data[0], row=9, col=1)

    fig.add_trace(plot_ichimoku_cloud(data).data[0], row=10, col=1)
    fig.add_trace(plot_ichimoku_cloud(data).data[1], row=10, col=1)
    fig.add_trace(plot_ichimoku_cloud(data).data[2], row=10, col=1)
    fig.add_trace(plot_ichimoku_cloud(data).data[3], row=10, col=1)
    fig.add_trace(plot_ichimoku_cloud(data).data[4], row=10, col=1)

    fig.add_trace(plot_vwap(data).data[0], row=11, col=1)

    fig.add_trace(plot_atr(data).data[0], row=12, col=1)

    fig.add_trace(plot_std_deviation(data).data[0], row=13, col=1)

    fig.add_trace(plot_mean_closing_price(data).data[0], row=14, col=1)

    fig.add_trace(plot_variance_closing_price(data).data[0], row=15, col=1)

    fig.add_trace(plot_coefficient_of_variation(data).data[0], row=16, col=1)

    # Обновление макета
    fig.update_layout(height=2000, title_text=f"{ticker} Цена акций с течением времени")

    # Сохранение графика в файл
    fig.write_html(full_path)
    print(f"График сохранен как {full_path}")
