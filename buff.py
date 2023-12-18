import requests
import time
from math import floor
import json


def get_dict_goods_id_name():
    """This function return dictionary connecting id and skin name

    Returns:
        dict['name'] = id
    """
    result = {}
    with open('data/buffids.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) == 2:
                goods_id, name = parts
                result[name] = goods_id
    return result


def get_price_from_buff_by_goods_id(goods_id):
    """This function gets the first(lowest) price from buff's api using goods_id
    Args:
        goods_id (int): to send a request, you need to know the skin id

    Returns:
        first_buffs_price_cny (float) 

    Note:
        Maybe it works without unix_time 
    """
    unix_time = floor(time.time() * 1000)
    res = requests.get(
        f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={goods_id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={unix_time}"
    )
    dt = res.json()
    first_buffs_price_cny = dt["data"]["items"][0]["price"]
    first_steam_price_cny = first_steam_price_cny = dt["data"]["goods_infos"][
        f'{goods_id}']["steam_price_cny"]
    return first_buffs_price_cny


def get_steam_and_buffs_price(goods_id):
    """Get steam's and buff's prices from buff api using goods id

    Args:
        goods_id (int): to send a request, you need to know the skin id

    Returns:
        first_buffs_price_cny(float)
        first_steam_price_cny(float)

    """
    unix_time = floor(time.time() * 1000)
    res = requests.get(
        f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={goods_id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_={unix_time}"
    )
    dt = res.json()
    first_buffs_price_cny = dt["data"]["items"][0]["price"]
    first_steam_price_cny = first_steam_price_cny = dt["data"]["goods_infos"][
        f'{goods_id}']["steam_price_cny"]
    return first_buffs_price_cny, first_steam_price_cny


if __name__ == "__main__":
    price, pr = get_price_from_buff_by_goods_id(33971)
    print(price, pr)
