def trade_to_dict(trade):
    return {
        "symbol": trade.get("symbol"),
        "strategy": trade.get("strategy"),
        "price": trade.get("price"),
        "index": trade.get("index"),
        "profit": trade.get("profit", 0),
        "timestamp": trade.get("timestamp")
    }
