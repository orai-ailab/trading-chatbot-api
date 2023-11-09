import requests
import os
from datetime import datetime, timedelta
import time
import json
import help
CENTIC_JWT_TOKEN = os.getenv("CENTIC_JWT_TOKEN")

def top_n_asset_performance(num_asset: int, criteria: str, interval: int):
    """
    Queries top num_asset of tokens based on criteria over interval.

    :param num_asset: Number of top-performing assets to return
    :param criteria: Performance criteria (marketCap, tradingVolume, tokenHealth, tradingVolumeChangeRate)
    :param interval: Time interval for performance, in days
    :return: List of dictionaries containing asset performance data
    """
    
    # Validate criteria
    valid_criteria = {"marketCap", "tradingVolume", "tokenHealth", "tradingVolumeChangeRate"}
    if criteria not in valid_criteria:
        raise ValueError(f"Criteria must be one of {valid_criteria}")

    # Construct the URL to get the list of top assets
    asset_list_query_url = (
        f"https://api-staging.centic.io/dev/v3/ranking/tokens"
        f"?order=desc&orderBy={criteria}&pageSize={num_asset}&duration={interval}"
    )

    # Fetch the asset list
    try:
        response = requests.get(asset_list_query_url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        asset_list = response.json().get('docs', [])
    except requests.RequestException as e:
        raise RuntimeError("Failed to fetch asset list") from e

    # Fetch analytics for each asset and update the asset information
    for asset in asset_list:
        asset_id = asset.get('id')
        asset_analytics_query_url = f"https://api-staging.centic.io/dev/v3/common/analytics?id={asset_id}&type=token"
        
        try:
            analytics_response = requests.get(asset_analytics_query_url)
            analytics_response.raise_for_status()  # Checks for HTTP errors
            asset_analytics = analytics_response.json()
            asset.update(asset_analytics)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch analytics for asset {asset_id}") from e

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

def portfolio_performance(wallet_address: str, interval: int):
    """
    Intent: ask_onchain/portfolio_performance
    Query credit score history for a specific wallet over a defined interval.
    
    Inputs:
        wallet_address: A string representing the wallet address to query.
        interval: An integer representing the interval in days.

    Outputs:
        A JSON-formatted string containing the credit score history for the specified wallet
        within the specified time interval.
    """
    wallet_url_api = f'https://api-staging.centic.io/dev/v3/credit-score/{wallet_address}/history'
    wallet_score_history = requests.get(wallet_url_api).json()
    timestamps_to_change = list(wallet_score_history["creditScoreHistory"].keys())
    for timestamp in timestamps_to_change:
        time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        wallet_score_history["creditScoreHistory"][time] = wallet_score_history["creditScoreHistory"].pop(timestamp
    
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



