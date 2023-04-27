import sqlite3
import pandas as pd

def fetch_from_db(code):
    con = sqlite3.connect("data/stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = con.cursor()

    cur.execute(f"SELECT name FROM code_master WHERE code='{code}'")
    name = cur.fetchone()[0]
    cur.execute(f"SELECT * FROM stock_data WHERE code='{code}'")
    dates, open_prices, close_prices, high_prices, low_prices, volumes = [], [], [], [], [], []
    for row in cur.fetchall():
        dates.append(row[1])
        open_prices.append(row[2])
        high_prices.append(row[3])
        low_prices.append(row[4])
        close_prices.append(row[5])
        volumes.append(row[6])
    st = pd.DataFrame({
        "Date":dates, "Open":open_prices, "High":high_prices,
        "Low":low_prices, "Close":close_prices, "Volume":volumes
    })
    st["Date"] = pd.to_datetime(st["Date"])
    st = st.sort_values(by="Date", ascending=True).reset_index(drop=True)

    return name, st

def fetch_from_db_with_condition(code, start_date, end_date):
    con = sqlite3.connect("data/stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = con.cursor()

    cur.execute(f"SELECT name FROM code_master WHERE code='{code}'")
    name = cur.fetchone()[0]
    cur.execute(f"SELECT * FROM stock_data WHERE code='{code}' AND date>='{start_date}' AND date<='{end_date}'")
    dates, open_prices, close_prices, high_prices, low_prices, volumes = [], [], [], [], [], []
    for row in cur.fetchall():
        dates.append(row[1])
        open_prices.append(row[2])
        high_prices.append(row[3])
        low_prices.append(row[4])
        close_prices.append(row[5])
        volumes.append(row[6])
    st = pd.DataFrame({
        "Open":open_prices, "High":high_prices,
        "Low":low_prices, "Close":close_prices, "Volume":volumes
    }, index=dates)
    st["Date"] = pd.to_datetime(st["Date"])
    st = st.sort_values(by="Date", ascending=True).reset_index(drop=True)

    return name, st