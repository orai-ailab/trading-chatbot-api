import requests
import os
import json
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
def portfolio_wallet(wallet_id: str, chainid: str):
    """
    Intent: ask_onchain/portfolio_wallet
    Query wallet overview data for a specific wallet on a given chain.

    Inputs:
        wallet_id: A string representing the wallet address to query.
        chainid: A string representing the chain ID for which the wallet overview is requested.

    Outputs:
        A JSON-formatted string containing wallet overview data.
        If there's an issue with the request or response, it returns None.
    """
    
    # Kiểm tra xem wallet_id và chainid có phải là chuỗi không
    if not isinstance(wallet_id, str) or not isinstance(chainid, str):
        raise ValueError("Invalid wallet address or chain ID.")

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

