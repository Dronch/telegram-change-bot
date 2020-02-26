import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import io

from typing import List

from .exchange_rate import ExchangeRate


def history_graph(history: List[ExchangeRate]) -> io.BytesIO:

    x, y, from_currency, to_currency = [], [], None, None
    for item in sorted(history, key=lambda i: i.date):
        x.append(item.date)
        y.append(item.rate)
        from_currency = item.from_currency
        to_currency = item.to_currency

    fig, ax = plt.subplots(figsize=(5, 3), tight_layout=True)
    ax.set_ylabel(f'{from_currency} - {to_currency}')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %b %d'))
    ax.tick_params(axis='x', rotation=70)

    ax.plot(x, y)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf
