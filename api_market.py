import requests
import csv
from pandas import DataFrame, read_csv
import pandas as pd
from time import gmtime, strftime
from shutil import move

url = 'https://market.csgo.com/api/v2/prices/class_instance/RUB.json'
real_time = strftime("%d_%m_%Y-%H:%M:%S", gmtime())


def get_prices_from_market():
    """Generate a csv file with prices from api market

    Returns:
        Error: status.code
    """
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        with open(f'skins_market_{real_time}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            row = ['name', 'mk_price', 'mk_avg_price', 'sales']
            writer.writerow(row)
            for item_id, item_data in data["items"].items():
                if item_data["popularity_7d"] is not None:
                    market_hash_name = item_data["market_hash_name"]
                    price = item_data["price"]
                    avg_price = item_data["avg_price"]
                    popularity_7d = item_data["popularity_7d"]
                    skin = [market_hash_name, price, avg_price, popularity_7d]
                    writer.writerow(skin)
    else:

        return response.status_code
    return 0


def custom_aggregation(group):
    """Collects duplicate records in a table - summarizes the number of sales,
    takes the lowest average price.
    
    Called in function delete_duplucate

    Returns:
        pd.Series: uniq skins name 
    """
    min_diff_idx = group['mk_avg_price'].idxmin()
    total_sales = group['sales'].sum()
    aggregated_data = {
        'name': group.loc[min_diff_idx, 'name'],
        'mk_avg_price': group.loc[min_diff_idx, 'mk_avg_price'],
        'mk_price': group.loc[min_diff_idx, 'mk_price'],
        'sales': total_sales
    }
    return pd.Series(aggregated_data,
                     index=['name', 'mk_avg_price', 'mk_price', 'sales'])


def delete_duplicate():
    """Delete duplicate from last csv with skins

    Returns:
        DataFrame: uniq column   
    """
    df = pd.read_csv(f"skins_market_{real_time}.csv")
    groups = df.groupby('name')
    result_df = groups.apply(custom_aggregation).reset_index(drop=True)
    return result_df


def prepare_markets_data(df, min_price, max_price, count_of_sales):
    """Removes records that do not match the query from the DataFrame.
    Removes raw CSV from /data

    Args:
        df (pd.DataFrame):
        count_of_sales (integer): these are the values ​​for filtering out unnecessary skins
    Returns:
        df (pd.DataFrame): filtered DataFrame
    """
    df = df.sort_values(by="sales", ascending=False)
    df = df.query(f"sales > {count_of_sales}")
    df = df[(df['mk_avg_price'] > min_price)
            & (df['mk_avg_price'] < max_price)]
    move(f"skins_market_{real_time}.csv", 'data')
    return df


def get_df_to_compare(min_price, max_price, count_of_sales):
    """
        function - collector, calls all filtering functions and adds new columns 
        3 - buff price, 4 - spread. New columns are filled with None
    Args:
    
    Returns:
        df: this dataframe is used to visualize data and make decisions about which skins to purchase
    """
    get_prices_from_market()
    df = delete_duplicate()
    df = prepare_markets_data(df, min_price, max_price, count_of_sales)
    df.insert(3, 'buff_price', None)
    df.insert(4, 'spread', None)
    return df


# функция для проверки правилности группировки
# def foo():
#     get_prices_from_market()
#     df = read_csv(f"skins_market_{real_time}.csv")
#     groups = df.groupby('name')
#     duplicates = groups.filter(lambda group: len(group) > 1)
#     print(duplicates.sort_values(by="name",ascending=False))

if __name__ == "__main__":
    get_df_to_compare()
