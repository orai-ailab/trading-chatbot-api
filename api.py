import requests
import os
from datetime import datetime, timedelta
import time
import json
import help
CENTIC_JWT_TOKEN = os.getenv("CENTIC_JWT_TOKEN")

def top_n_asset_performance(num_asset:int, criteria:str, interval:int):
    r"""
    Intent: ask_onchain/top_n_asset_performance
    Query top num_asset of tokens based on criteria over interval
    Input:
        num_asset
        criteria: in ["marketCap", "tradingVolume", "tokenHealth", "tradingVolumeChangeRate"]
        interval: by days
    Output:
        Everything is obvious except:
        "asset": Key: UNIX timestamp according to the interval specification, Value: total amount of tokens hold as asset (in wallets across all chains supported).

        "performance": Key, same as above, Value: percentage of total value increase/decrease w.r.t to the previous timestamp 
        "dailyPAndL": Key, same as above, Value: Profit/Loss based on market price at the time, w.r.t to the previous timestamp
        "cumulativePAndL": ...
        "greatEvents": array of this token transfer of significant amount
        "exchanges": arrray of this token amount over different exchanges
    """

    if criteria in ["marketCap", "tradingVolume", "tokenHealth", "tradingVolumeChangeRate"]:
        pass
    else:
        raise

    asset_list_query_url = f"https://api-staging.centic.io/dev/v3/ranking/tokens?order=desc&orderBy={criteria}&pageSize={num_asset}&duration={interval}"
    asset_list = requests.get(asset_list_query_url).json()['docs']

    for i in range(len(asset_list)):
        asset_id = asset_list[i]['id']
        asset_analytics_query_url = f"https://api-staging.centic.io/dev/v3/common/analytics?id={asset_id}&type=token"
        asset_analytics = requests.get(asset_analytics_query_url).json()
        asset_list[i].update(asset_analytics)

    return asset_list


def portfolio_asset(wallet_address: str, interval: int):
    """
    Intent: ask_onchain/portfolio_asset
    Query and update the asset portfolio summary for a specific wallet.

    Inputs:
        wallet_address: A string representing the wallet address to query.
        interval: An integer representing the interval in days.

    Outputs:
        A dictionary containing the updated asset portfolio history of the specified wallet.
        If there's an issue with the request or response, it returns None.
    """
    summary_asset_wallet_API = f"https://api-staging.centic.io/dev/v3/credit-score/{wallet_address}/detail"
    
    response = requests.get(summary_asset_wallet_API)
    
    if response.status_code == 200:
        data = response.json()
    else:
        return None

    assets = data["assets"]
    fields_to_move = {
        "totalAssets": assets["totalAssets"],
        "avgTotalAssets": assets["avgTotalAssets"],
        "totalBalance": assets["totalBalance"],
        "avgTotalBalance": assets["avgTotalBalance"],
        "totalDeposit": assets["totalDeposit"],
        "investmentRatio": assets["investmentRatio"],
        "totalBorrow": assets["totalBorrow"],
        "loanRatio": assets["loanRatio"]
    }
    
    data["assets"]["assetsHistory"][current_time] = fields_to_move
    for field in fields_to_move:
        del data["assets"][field]
    timestamps_to_change = list(data["assets"]["assetsHistory"].keys())
    for timestamp in timestamps_to_change:
        time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        if timestamp in data["assets"]["assetsHistory"]:
         time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
         data["assets"]["assetsHistory"][time] = data["assets"]["assetsHistory"].pop(timestamp)
    end_date = datetime.now() - timedelta(days=interval + 1)
    values_in_range = {}
    for time, data_point in data["assets"]["assetsHistory"].items():
        time_date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if time_date >= end_date:
            values_in_range[time] = data_point
    return json.dumps(values_in_range, indent=2)


def portfolio_performance(wallet_id: str, interval: int):
    """
    Intent: ask_onchain/
    Query credit score history for a specific wallet over a defined interval.
    
    Inputs:
        wallet_id: A string representing the wallet address to query.
        interval: An integer representing the interval in days.

    Outputs:
        A JSON-formatted string containing the credit score history for the specified wallet
        within the specified time interval.
    """
    if not isinstance(wallet_id, str):
        return "Invalid wallet address."

    elif not isinstance(interval, int) or interval < 0:
        return "Invalid Interval"
    wallet_url_api = f'https://api-staging.centic.io/dev/v3/credit-score/{wallet_id}/history'
    wallet_score_history = requests.get(wallet_url_api).json()
    timestamps_to_change = list(wallet_score_history["creditScoreHistory"].keys())
    for timestamp in timestamps_to_change:
        time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        wallet_score_history["creditScoreHistory"][time] = wallet_score_history["creditScoreHistory"].pop(timestamp)
    end_date = datetime.now() - timedelta(days=interval + 1)
    values_in_range = {}
    for time, data_point in wallet_score_history["creditScoreHistory"].items():
        time_date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if time_date >= end_date:
            values_in_range[time] = data_point
    return json.dumps(values_in_range, indent=2)


def portfolio_wallet(wallet_address: str, chainid: str):
    """
    Intent: ask_onchain/portfolio_wallet
    Query wallet overview data for a specific wallet on a given chain.

    Inputs:
        wallet_address: A string representing the wallet address to query.
        chainid: A string representing the chain ID for which the wallet overview is requested.

    Outputs:
        A JSON-formatted string containing wallet overview data.
        If there's an issue with the request or response, it returns None.
    """
    overview_API = f"https://api-staging.centic.io/dev/v3/wallets/{wallet_id}/overview?chain={chainid}"
    
    response = requests.get(overview_API)
    
    if response.status_code == 200:
        data = response.json()
        tokens = data['tokens']
        nfts = data["nfts"]
        dapps = data["dapps"]
        lastUpdatedAt = data["lastUpdatedAt"]
        result = {
            "tokens": tokens,
            "nfts": nfts,
            "dapps": dapps,
            "lastUpdatedAt": lastUpdatedAt
        }
        return json.dumps(result, indent=2)
    else:
        return None


def get_coin_history(coin_name: str, currency: str, day: int):
    """
    Purpose: Retrieve historical prices of a cryptocurrency through the CoinGecko API
    Input:
        coin_name: Name of the cryptocurrency
        currency: The currency for the price (e.g., usd, vnd)
        day: Number of days of historical data (2-90)
    Output:
        Returns historical prices for the specified cryptocurrency or raises an exception on error
    """
    # First, map the coin name to coin_id using the map_coin_id function
    coin_id = help.map_coin_id(coin_name)
    
    if coin_id == "Not Found Coin":
        raise Exception(f"Coin with name '{coin_name}' not found")
    
    # Use the coin_id to fetch historical data
    coin_API = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currency}&days={day}&interval=daily"
    response = requests.get(coin_API)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")



