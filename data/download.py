import argparse
import yfinance
import sqlite3
from datetime import date
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="全範囲取得か差分取得")
    parser.add_argument("type", help="全範囲取得(all)か差分取得(diff)")
    args = parser.parse_args()

    conn = sqlite3.connect("stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    latest_date = None
    today = date.today()
    codes = []
    with open("target.txt", "r") as f:
        for line in f:
            codes.append(line.rstrip("\n"))
    for code in codes:
        if args.type == "all":
            try:
                stock_data = yfinance.download(code, period="max")
                cur.execute(f"select name from code_master where code='{code}'")
            except:
                cur.execute(f"DELETE FROM code_master WHERE code = '{code}'")
            else:
                for index, row in stock_data.iterrows():
                    bus_date = index.to_pydatetime().date()
                    open_price = row['Open']
                    high_price = row['High']
                    low_price = row['Low']
                    close_price = row['Close']
                    volume = row['Volume']
                    cur.execute("INSERT INTO stock_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (code, bus_date, open_price, high_price, low_price, close_price, volume))
            finally:    
                conn.commit()
        elif args["type"] == "diff":
            if latest_date is None:
                cur.execute(f"SELECT date FROM stock_data WHERE code='{code}'")
                dates = [row[0] for row in cur.fetchall()]
                latest_date = min(dates)
            try:
                stock_data = yfinance.download(code, start=latest_date, end=today)
            except:
                print(f"{code} does not have data between {latest_date} and {today}.")
            else:
                for index, row in stock_data.iterrows():
                    bus_date = index.to_pydatetime().date()
                    open_price = row['Open']
                    high_price = row['High']
                    low_price = row['Low']
                    close_price = row['Close']
                    volume = row['Volume']
                    cur.execute("INSERT INTO stock_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (code, bus_date, open_price, high_price, low_price, close_price, volume))
                    conn.commit()
    conn.close()