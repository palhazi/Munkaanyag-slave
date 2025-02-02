import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 1. Adatok letöltése a Yahoo Finance-ből
ticker = "AAPL"  # Példa részvény: Apple
df = yf.download(ticker, period="1y")  # 1 évnyi adat letöltése

# Ellenőrizd a letöltött adatokat
print(df.head())

# 2. Adatok előkészítése
# Használj másik oszlopot, ha az 'Adj Close' nem létezik
if 'Adj Close' in df.columns:
    df['Prediction'] = df['Adj Close'].shift(-1)  # Előző napi ár eltolva egy nappal
elif 'Close' in df.columns:
    df['Prediction'] = df['Close'].shift(-1)  # Előző napi ár eltolva egy nappal
else:
    raise KeyError("Neither 'Adj Close' nor 'Close' columns found in the data.")

df.dropna(inplace=True)  # NaN értékek eltávolítása

X = df[['Adj Close']] if 'Adj Close' in df.columns else df[['Close']]  # Független változó
y = df['Prediction']   # Függő változó

# 3. Adatok felosztása tanító és teszt adatokra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Modell létrehozása és tanítása
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Modell értékelése
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse}")

# 6. Predikciók készítése (példa)
last_day_price = df['Adj Close'].iloc[-1] if 'Adj Close' in df.columns else df['Close'].iloc[-1]
# A predikció bemenetét DataFrame-ként adjuk át az oszlopnévvel
future_input = pd.DataFrame([[last_day_price]], columns=["Adj Close"] if 'Adj Close' in df.columns else ["Close"])
future_prediction = model.predict(future_input)
print(f"Holnapi ár előrejelzése: {future_prediction[0]}")

# Grafikus megjelenítés (opcionális)
plt.plot(X_test, y_test, label="Actual")
plt.plot(X_test, y_pred, label="Predicted")
plt.legend()
plt.show()

