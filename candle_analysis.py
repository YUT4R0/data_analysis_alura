import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_share(ticker, start, end):
    return yf.download(ticker, start=start, end=end)


petro_data = get_share("PETR4.SA", "2023-01-01", "2023-12-31")
apple_data = get_share("AAPL", "2023-01-01", "2023-12-31")
print(petro_data.columns)
close_graph = petro_data["Close"]
asset = pd.DataFrame(close_graph)
plt.plot(asset)
plt.title("Variacao do preco por dia")
plt.legend(["Fechamento"])
plt.show()

df = petro_data.head(60).copy()
# convertendo indice em uma coluna de data
df["Date"] = df.index
# convertendo as datas para o formato numerico de matplotlib (isso pra ele plotar as datas corretamente)
df["Date"] = df["Date"].apply(mdates.date2num)

# candle graph
fig, ax = plt.subplots()
width = 0.8

for i in range(len(df)):
    if df["Close"].iloc[i] > df["Open"].iloc[i]:
        color = "green"
    else:
        color = "red"

    ax.plot(
        [df["Date"].iloc[i], df["Date"].iloc[i]],
        [df["Low"].iloc[i], df["High"].iloc[i]],
        color=color, linewidth=0.6
    )

    ax.add_patch(plt.Rectangle(
        (df["Date"].iloc[i] - width / 2,
         min(df["Open"].iloc[i], df["Close"].iloc[i])),
        width,
        abs(df["Close"].iloc[i] - df["Open"].iloc[i]),
        facecolor=color
    ))

# media movel
df["MA7"] = df["Close"].rolling(window=7).mean()
df["MA14"] = df["Close"].rolling(window=14).mean()

ax.plot(df["Date"], df["MA7"], color="orange", label="Media movel de 7 dias")
ax.plot(df["Date"], df["MA14"], color="yellow", label="Media movel de 14 dias")
ax.legend()

# formatando eixos pra mostrar datas
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)
# adicionando titulos e rotulos pros eixos x e y
plt.title("PETR4.SA - Candlestick graph")
plt.xlabel("Data")
plt.ylabel("Preco")
plt.grid(True)

plt.show()

# subplots
fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True,
    vertical_spacing=0.1,
    subplot_titles=("Candlestick", "Volume transacionado"),
    row_width=[0.2, 0.7]
)

# adding graph to candtlestick
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Candlestick"),
    row=1, col=1)

# adding media movel to subplot
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["MA7"],
    mode="lines",
    name="MA7 - Media movel 7 dias"),
    row=1, col=1
)

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["MA14"],
    mode="lines",
    name="MA14 - Media movel 14 dias"),
    row=1, col=1
)
# adding bar graph to volume
fig.add_trace(go.Bar(
    x=df.index,
    y=df["Volume"],
    name="Volume"),
    row=2, col=1
)
# update layout
fig.update_layout(
    yaxis_title="Preco",
    xaxis_rangeslider_visible=False
)

fig.show()
# petro mpf candle
mpf.plot(
    petro_data.head(30),
    type="candle",
    volume=True,
    mav=(7, 14),
    style="yahoo"
)
# apple mpf candle
mpf.plot(
    apple_data.head(30),
    type="candle",
    volume=True,
    mav=(7, 14),
    style="yahoo"
)
