import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet


def get_share(ticker, start, end, progress):
    return yf.download(ticker, start=start, end=end, progress=progress)


data = get_share("JNJ", "2020-01-01", "2023-12-31", False)
data = data.reset_index()
print(data.columns)

training_data = data[data["Date"] < "2023-07-31"]
testing_data = data[data["Date"] >= "2023-07-31"]
# training data = ds, prediction target = y
prophet_training_data = (training_data[["Date", "Close"]]
                         .rename(columns={"Date": "ds", "Close": "y"}))
# create and train model
model = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=False)
model.add_country_holidays(country_name='US')
model.fit(prophet_training_data)
# create future dates for prediction until the end of 2023
future = model.make_future_dataframe(periods=150)
prediction = model.predict(future)
# plots training, test and prediction data
plt.plot(training_data["Date"], training_data["Close"], label="Training Data", color="blue")
plt.plot(testing_data["Date"], testing_data["Close"], label="Real Data (test)", color="green")
plt.plot(prediction["ds"], prediction["yhat"], label="Prediction", color="orange", linestyle="--")

plt.axvline(training_data["Date"].max(), color='red', linestyle='--', label='Prediction start')
plt.xlabel("Date")
plt.ylabel("Preco de fechamento")
plt.title("Previsao de preco de fechamento VS Dados reais")
plt.legend()
plt.xticks(rotation=45)
plt.show()
