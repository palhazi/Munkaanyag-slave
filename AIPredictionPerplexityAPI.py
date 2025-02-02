import asyncio
import aiohttp
from openai import OpenAI
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pytz
import numpy as np
from sklearn.linear_model import LinearRegression

class SP500NewsAnalyzer:
    def __init__(self, api_key):
        # Itt add meg a saját Perplexity API kulcsodat!
        self.client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        self.sources = [
            "https://www.wsj.com/market-data/quotes/index/SPX",
            "https://www.reuters.com/markets/us/",
            "https://www.cnbc.com/quotes/.SPX",
            "https://www.bloomberg.com/quote/SPX:IND"
        ]
        
    async def fetch_news(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def gather_news(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_news(session, url) for url in self.sources]
            return await asyncio.gather(*tasks)

    def parse_news(self, html_contents):
        news_items = []
        for html in html_contents:
            soup = BeautifulSoup(html, 'html.parser')
            # Próbáljuk meg kikeresni a hír címeket; szükség esetén módosítsd a keresési szelektort!
            headlines = soup.find_all('h2', class_='headline')
            for headline in headlines:
                news_items.append(headline.text.strip())
        return news_items

    def analyze_sentiment(self, news_items):
        if not news_items:
            print("No news items found to analyze.")
            return 0.0
        combined_news = " ".join(news_items)
        response = self.client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": "Analyze the sentiment of news related to the S&P 500."},
                {"role": "user", "content": f"Analyze the sentiment of the following news related to the S&P 500 and provide a rating between -1 (very negative) and 1 (very positive): '{combined_news}'"}
            ]
        )
        try:
            return float(response.choices[0].message.content)
        except ValueError:
            print("Could not convert the API response to a float. Response was:")
            print(response.choices[0].message.content)
            return 0.0  # Return a neutral sentiment score

    def predict_future_trend(self, sentiment_score):
        current_price = 6067.70  # Current value of S&P 500 (példaérték)
        # Generálunk egy véletlenszerű történelmi adatot
        historical_data = pd.DataFrame({
            'Date': pd.date_range(end=datetime.now(pytz.timezone('US/Eastern')), periods=30),
            'Price': np.random.normal(current_price, 50, 30)
        })
        
        X = np.array(range(len(historical_data))).reshape(-1, 1)
        y = historical_data['Price']
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_dates = pd.date_range(start=datetime.now(pytz.timezone('US/Eastern')), periods=7)
        future_X = np.array(range(len(historical_data), len(historical_data) + 7)).reshape(-1, 1)
        
        predictions = model.predict(future_X)
        # A hangulat hatását beépítjük: enyhén módosítjuk az előrejelzést
        predictions *= (1 + 0.01 * sentiment_score)
        
        return pd.DataFrame({'Date': future_dates, 'Predicted_Price': predictions})

    async def run_analysis(self):
        html_contents = await self.gather_news()
        news_items = self.parse_news(html_contents)
        sentiment_score = self.analyze_sentiment(news_items)
        future_predictions = self.predict_future_trend(sentiment_score)
        
        summary = f"""
Latest news for S&P 500:
{' '.join(news_items[:5])}

News sentiment score: {sentiment_score}

Future outlook:
{future_predictions.to_string(index=False)}
"""
        return summary

async def main():
    # Cseréld ki az alábbi üres stringet a saját API kulcsodra!
    analyzer = SP500NewsAnalyzer("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")
    result = await analyzer.run_analysis()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
