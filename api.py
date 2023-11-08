import requests
import os

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

