import requests


def get_price(url, params):
    """Fetches trade data from the specified Huobi API endpoint and calculates the average prices for buy and sell trades.

    Args:
        url (str): The API endpoint URL.
        params (dict): Parameters for the API request.

    Returns:
        tuple: A tuple containing the average prices for buy and sell trades.
    """
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get('data', [])

        buy_price_total, sell_price_total = 0, 0
        buy_count, sell_count = 0, 0

        for item in data:
            trades = item.get('data', [])

            for trade_data in trades:
                direction = trade_data.get('direction', '')
                price = trade_data.get('price', 0)

                if direction == 'buy':
                    buy_price_total += price
                    buy_count += 1
                elif direction == 'sell':
                    sell_price_total += price
                    sell_count += 1

        average_buy_price = buy_price_total / buy_count if buy_count > 0 else 0
        average_sell_price = sell_price_total / sell_count if sell_count > 0 else 0

        return round(average_buy_price, 2), round(average_sell_price, 2)
    else:
        raise TimeoutError


url = 'https://api.huobi.pro/market/history/trade'
params = {'symbol': 'usdtrub', 'size': 100}
get_price(url, params)
