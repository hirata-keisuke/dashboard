def calc_stochastics(st, n, m):
    """ストキャスティクスを計算する
    
    Args:
        st (pandas.DataFrame):株式情報
        n (int):%Kの期間
        m (int):%Dの期間
        
    Returns:
        ndarray:%Kの配列
        ndarray:%Dの配列
    """
    # ストキャスティックスを計算するために必要なデータを準備する
    high = st["High"]
    low = st["Low"]
    close = st["Close"]

    # %Kを計算する
    min_low = low.rolling(window=n).min()
    max_high = high.rolling(window=n).max()
    k = (close - min_low) / (max_high - min_low) * 100

    # %Dを計算する
    d = k.rolling(window=m).mean()

    # 結果をDataFrameに格納する
    return k.to_numpy(), d.to_numpy()

def assess(k_value, d_value):
    assessment = ""
    if k_value>=70 and d_value>=70:
        assessment = "買われすぎている\n"+f"%K:{k_value:.1f}, %D:{d_value:.1f}"
    elif k_value<=30 and d_value<=30:
        assessment = "売られすぎている\n"+f"%K:{k_value:.1f}, %D:{d_value:.1f}"
    else:
        assessment = "中間的であろう\n"+f"%K:{k_value:.1f}, %D:{d_value:.1f}"
    return assessment