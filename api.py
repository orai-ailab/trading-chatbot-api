import requests

def top_n_asset_performance(num_asset:int, criteria:str, interval:int):
    r"""
    Intent: ask_onchain/top_n_asset_performance
    Query top num_asset of tokens based on criteria over interval
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

