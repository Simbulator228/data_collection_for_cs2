from api_market import get_df_to_compare
import buff
import pandas as pd
import logging

log_file = "error_log.txt"
logging.basicConfig(filename=log_file,
                    level=logging.ERROR,
                    format="%(asctime)s - %(message)s")


def update_dataframe_with_buff_price(df, course_cny_rub):
    """
    Update the given DataFrame with Buff prices and calculate the spread.

    Args:
        df (pd.DataFrame): The DataFrame containing product information.
        course_cny_rub (float): The exchange rate from CNY to RUB.

    Returns:
        pd.DataFrame: The updated DataFrame.
    """
    for goods_id in df.index:
        try:
            buff_price = float(buff.get_price_from_buff_by_goods_id(goods_id))
            df.at[goods_id, 'buff_price'] = round(buff_price * course_cny_rub,
                                                  2)

            df.at[goods_id,
                  'spread'] = ((df.at[goods_id, 'mk_avg_price'] * 0.9025 -
                                df.at[goods_id, 'buff_price']) /
                               df.at[goods_id, 'buff_price'] * 100).round(2)
        except Exception as e:
            df.at[goods_id, 'buff_price'] = None
            df.at[goods_id, 'spread'] = None
            logging.error(f"Error processing goods_id {goods_id}: {str(e)}")

        print(df.loc[goods_id])  # For debugging purposes

    return df


if __name__ == "__main__":
    min_price_threshold = 1500
    max_price_threshold = 4000
    count_of_sales_threshold = 20
    exchange_rate_cny_rub = 13.46

    df = get_df_to_compare(min_price_threshold, max_price_threshold,
                           count_of_sales_threshold)

    new_indices_dict = buff.get_dict_goods_id_name()
    df.set_index(df['name'].map(new_indices_dict), inplace=True)

    df = update_dataframe_with_buff_price(df, exchange_rate_cny_rub)

    df = df.sort_values(by="spread", ascending=False)

    df.to_csv('result.csv')