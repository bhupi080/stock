import argparse
from fastapi import FastAPI, HTTPException
import uvicorn
import yfinance as yf
from fastapi.encoders import jsonable_encoder
import uvicorn
import os

app = FastAPI()

app = FastAPI(
    title="Stock API - Coredge.io Task 1",
    description="An API to fetch stock market data and calculate SMA",
    version="1.0.0",
    task_link="https://gist.github.com/EXTREMOPHILARUM/f0af6d81ae9eb557aab34dd03e61c974",
    contact={
        "name": "bhupinder kumar",
        "email": "bhupisingh080@gmail.com",
        "url": "https://bhupisingh.in",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Stock Data API")
parser.add_argument("--sma_window", type=int, default=20, help="SMA window size (default: 20)")
parser.add_argument("--period", type=str, default="1mo", help='Stock data period (e.g., "1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")')
args = parser.parse_args()

# In-memory storage for processed tickers
history_store = []

@app.post("/process/{ticker}",tags=["Stock Processing"])
async def process_ticker(ticker: str):
    try:
        # Fetch last ~30 days of daily historical data
        stock_data = yf.Ticker(ticker)
        stock_data = stock_data.history(period=args.period)
        print(type(stock_data))
        if stock_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")

        # Select relevant columns and reset index
        stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
        stock_data.reset_index(inplace=True)

        # Calculate 20-day SMA
        stock_data[f"SMA_{args.sma_window}"] = stock_data['Close'].rolling(window=args.sma_window).mean().shift(1)


        # Get latest available date
        latest_row = stock_data.iloc[-1]
        latest_date = latest_row['Date'].strftime('%Y-%m-%d')
        latest_close = latest_row['Close']
        latest_sma = latest_row[f"SMA_{args.sma_window}"]

        # Store in history (max 5 unique tickers)
        history_store.append({
            "ticker": ticker.upper(),
            "latest_date": latest_date,
            "closing_price": latest_close,
            f"sma_{args.sma_window}": latest_sma
        })
        if len(history_store) > 5:
            history_store.pop(0)
        # Convert DataFrame to JSON response
        # json_data = df.to_dict(orient="records")
        # return jsonable_encoder({"ticker": ticker, "data": json_data})
        return jsonable_encoder({
            "ticker": ticker.upper(),
            "latest_date": latest_date,
            "closing_price": latest_close,
            f"sma_{args.sma_window}": latest_sma
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", tags=["Stock History"])
async def get_history():
    return {
        "total_count": len(history_store),
        "history": history_store
    }

# @app.get("/history/{ticker}")
# def get_stock_history(ticker: str):
#     """
#     Fetches the last 30 days of daily stock data for the given ticker.
#     """
   
#     try:
#         # Get today's and past 30 days' date
#         # end_date = datetime.today().strftime('%Y-%m-%d')
#         # start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

#         # Fetch data from Yahoo Finance
#         df = yf.Ticker(ticker).history(period=args.period)
#         # df = stock.history(start=start_date, end=end_date)
        

#         if df.empty:
#             return {"error": "No data found for this ticker"}

#         # Select required columns & reset index to make 'Date' a column
#         df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
#         df.reset_index(inplace=True)

#         # Convert DataFrame to JSON response
#         json_data = df.to_dict(orient="records")
#         return jsonable_encoder({"ticker": ticker, "data": json_data})

#     except Exception as e:
#         return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
    # host = os.environ.get("HOST", "0.0.0.0")  # Default: 0.0.0.0
    # port = int(os.environ.get("PORT", 8000))  # Default: 8000
    # uvicorn.run("main:app", host=host, port=port)