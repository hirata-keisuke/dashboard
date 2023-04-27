def calc_sma(st, n):
    """単純移動平均線を計算する
    
    Args:
        st (pandas.DataFrame):株式情報
        n (int):平均を取る期間
    
    Returns:
        ndarray:単純移動平均値
    
    """

    return st["Close"].rolling(window=n).mean()

def find_GC_or_DC(st, short_window, long_window):
    """直近3日でゴールデンクロスもしくはデッドクロスが起きている日を探す
    """
    short_sma = calc_sma(st, short_window)
    long_sma = calc_sma(st, long_window)

    # ゴールデンクロスの判定
    buy_signal = (short_sma > long_sma) & (short_sma.shift(1) < long_sma.shift(1))

    # デッドクロスの判定
    sell_signal = (short_sma < long_sma) & (short_sma.shift(1) > long_sma.shift(1))

    GC_or_DC = ""
    for i in range(len(st)-3, len(st)):
        if buy_signal[i] and not sell_signal[i]:
            GC_or_DC = "GC"
            break
        elif sell_signal[i] and not buy_signal[i]:
            GC_or_DC = "DC"
            break

    return GC_or_DC