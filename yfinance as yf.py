import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 1. Adatok letöltése a Yahoo Finance-ből
ticker = "AAPL"  # Példa részvény: Apple
# auto_adjust=True: a "Close" oszlop már az igazított árakat tartalmazza
df = yf.download(ticker, period="1y", auto_adjust=True)  # 1 évnyi adat letöltése

# 2. Adatok előkészítése
# Az előző napi ár alapján próbáljuk megjósolni a mai árat,
# ezért a "Close" oszlop alapján készítjük a Prediction oszlopot.
df['Prediction'] = df['Close'].shift(-1)
df.dropna(inplace=True)  # NaN értékek eltávolítása

X = df[['Close']]    # Független változó (az előző napi ár)
y = df['Prediction'] # Függő változó (a mai ár)

# 3. Adatok felosztása tanító és teszt adatokra (80% tanító, 20% teszt)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Modell létrehozása és tanítása
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Modell értékelése
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # RMSE számítása
print(f"RMSE: {rmse}")

# 6. Predikciók készítése (példa)
last_day_price = df['Close'].iloc[-1]
# Az input DataFrame oszlopának nevének meg kell egyeznie a tanító adatokéval
future_input = pd.DataFrame([[last_day_price]], columns=["Close"])
future_prediction = model.predict(future_input)
print(f"Holnapi ár előrejelzése: {future_prediction[0]}")

# Grafikus megjelenítés (opcionális)
plt.plot(X_test, y_test, label="Actual")
plt.plot(X_test, y_pred, label="Predicted")
plt.legend()
plt.show()
