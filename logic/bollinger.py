def calc_sigma(st, n):
    """n日間の株価の標準偏差を計算する
    
    Args:
        st (pandas.DataFrame):株式情報
        n (int):標準偏差を計算する期間
        
    Returns:
        ndarray:株価の標準偏差
        
    """

    return st["Close"].rolling(window=n).std().to_numpy()