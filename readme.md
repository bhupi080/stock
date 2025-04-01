# FastAPI Stock Data API

This project is a stock market data analysis task that fetches stock data, calculates a Simple Moving Average (SMA), and provides an API to retrieve the processed data.

## 📌 Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Data Source:** Yahoo Finance (`yfinance`)
- **Dependencies:** `fastapi`, `uvicorn`, `pandas`, `yfinance`

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/bhupi080/stock.git
cd <repository_name>
```

### 2️⃣ Create & Activate Virtual Environment (Optional but Recommended)
#### For Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

---

## ▶️ Running the FastAPI Server
```sh
main:app --reload
```

- The server will run on `http://127.0.0.1:8000`
- Open `http://127.0.0.1:8000/docs` for Swagger UI.
- Open `http://127.0.0.1:8000/redoc` for ReDoc UI.

---

## 📌 API Endpoints

### 1️⃣ Process Stock Data
**POST /process/{ticker}**  
Fetches stock data, calculates a Simple Moving Average (SMA), and stores recent queries.

Response Example:
json
{
  "latest_date": "2024-04-01",
  "closing_price": 178.54,
  "sma_20": 175.23
}


### 2️⃣ Get Processed History
**GET /history**  
Returns a list of the last 5 processed tickers.

---

## 🛠 Customizing the API Docs
To change the default title and description of the Swagger UI, modify `main.py`:
```python
app = FastAPI(
    title="Stock Data API",
    description="Fetch stock market data and calculate technical indicators.",
    version="1.0.0"
)
```

---


---

## 📜 License
This project is licensed under the MIT License.

