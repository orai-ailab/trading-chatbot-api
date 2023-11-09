def map_coin_id(coin_name: str):
    """
    Purpose: Map a cryptocurrency's name to its unique identifier (coin_id) using the CoinGecko API.
    Input:
        coin_name: Name of the cryptocurrency
    Output:
        Returns the coin_id if the cryptocurrency is found in the CoinGecko database, or "Not Found Coin" if not found.
    """
    # Construct the API URL to fetch the list of cryptocurrencies
    list_coin_api = "https://api.coingecko.com/api/v3/coins/list"
    # Send a GET request to the CoinGecko API and parse the response as JSON
    list_coin = requests.get(list_coin_api).json()
    # Iterate through the list of cryptocurrencies to find a match based on name
    for coin_data in list_coin:
        if coin_data['name'].lower() == coin_name.lower():
            return coin_data['id']
    # Return "Not Found Coin" if the cryptocurrency is not in the database
    return "Not Found Coin"
