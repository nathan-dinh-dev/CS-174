from flask import Flask, request, jsonify, render_template
import sqlite3
import requests
from datetime import datetime, timedelta
import json
from flask_cors import CORS

app = Flask(__name__)
app = Flask(__name__, static_url_path="/static", static_folder="static")
CORS(app)
TIINGO_TOKEN = "3d984f8a243e99b9c80381f32199b3a8b932cd2a"
DATABASE = "search_history.db"


# ---------- Database Initialization ----------
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS SearchHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS CachedStockData (
                ticker TEXT PRIMARY KEY,
                company_json TEXT,
                stock_json TEXT,
                last_updated DATETIME
            )
        """
        )


init_db()


# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    ticker = request.args.get("ticker", "").upper().strip()
    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # # # Check cache
        cur.execute("SELECT * FROM CachedStockData WHERE ticker = ?", (ticker,))
        row = cur.fetchone()
        if row:
            last_updated = datetime.fromisoformat(row["last_updated"])
            if datetime.now() - last_updated < timedelta(minutes=15):
                return jsonify(
                    {
                        "company": json.loads(row["company_json"]),
                        "stock": json.loads(row["stock_json"]),
                        "from_cache": True,
                    }
                )

        print("Cache miss, fetching from Tiingo API...")
        # Fetch from Tiingo API
        headers = {"Content-Type": "application/json"}
        try:
            company_url = (
                f"https://api.tiingo.com/tiingo/daily/{ticker}?token={TIINGO_TOKEN}"
            )
            stock_url = f"https://api.tiingo.com/iex/{ticker}?token={TIINGO_TOKEN}"
            company_res = requests.get(company_url, headers=headers)
            stock_res = requests.get(stock_url, headers=headers)

            if company_res.status_code != 200 or stock_res.status_code != 200:
                return (
                    jsonify(
                        {
                            "error": "Error: No record has been found, please enter a valid symbol."
                        }
                    ),
                    404,
                )

            company_data = company_res.json()
            stock_data = stock_res.json()[0]

            # Save to cache
            cur.execute(
                """
                INSERT OR REPLACE INTO CachedStockData (ticker, company_json, stock_json, last_updated)
                VALUES (?, ?, ?, ?)
            """,
                (
                    ticker,
                    json.dumps(company_data),
                    json.dumps(stock_data),
                    datetime.now().isoformat(),
                ),
            )

            # Save to history
            cur.execute("INSERT INTO SearchHistory (ticker) VALUES (?)", (ticker,))
            conn.commit()

            return jsonify(
                {"company": company_data, "stock": stock_data, "from_cache": False}
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT ticker, timestamp FROM SearchHistory ORDER BY timestamp DESC LIMIT 10"
        )
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=True)
