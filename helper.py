import requests
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
    for coin_data in list_coin:
        if coin_data['name'].lower() == coin_name.lower():
            return coin_data['id']
    return "Not Found Coin"
def convert_time_to_day(data: dict):
    """
    Intent: Convert timestamp format and retain unique values based on the maximum timestamp per day.

    Inputs:
        data: A dictionary where timestamps are used as keys, and corresponding values are associated.

    Outputs:
        A new dictionary with timestamps converted to a different format, and values retained uniquely per day, keeping the value with the maximum timestamp for each day.

    Description:
        This function iterates through the input dictionary 'data' and converts the timestamp format to a new format. It then retains only unique values per day, ensuring that for each day, only the value with the maximum timestamp is kept. This helps to condense and organize the data by removing duplicate values for the same day, keeping the most recent information.
    """
    formatted_data = {}

    for timestamp, values in data.items():
        date_object = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        formatted_date = date_object.strftime("%Y-%m-%d")

        if formatted_date not in formatted_data:
            formatted_data[formatted_date] = values
        else:
            existing_timestamp = datetime.datetime.strptime(formatted_data[formatted_date].get('timestamp', '2000-01-01 00:00:00'), "%Y-%m-%d %H:%M:%S")
            current_timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            if current_timestamp > existing_timestamp:
                formatted_data[formatted_date] = values

    return formatted_data


def change_timestamp_format(dict_history: dict):
    """
    Intent : Convert timestamps to a Year-month-day.

    Inputs:
        dict_history: A dictionary with timestamps to be converted.

    Outputs:
        A new dictionary with timestamps formatted in a different way.
    """
    new_dict_history = {}
    for timestamp, data_point in dict_history.items():
        time_format = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        new_dict_history[time_format] = data_point
    return new_dict_history
def filter_values_by_interval(dict_history: dict, interval: int):
    """
    Intent: Filter values based on a time interval.

    Inputs:
        dict_history: A dictionary containing timestamps to be filtered.
        interval: The time interval for filtering.

    Outputs:
        A dictionary containing values within the specified time range.
    """
    end_date = datetime.now() - timedelta(days=interval + 1)
    values_in_range = {}
    for time, data_point in dict_history.items():
        time_date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if time_date >= end_date:
            values_in_range[time] = data_point
    return values_in_range


def process_data(data, keys, interval: int):
    """
    Intent: Perform key changes and filter values by time for a specific part of the data.

    Inputs:
        data: The data to be processed.
        keys: A list of keys to access the nested parts of the data to be processed.
        interval: The time interval for value filtering.

    Outputs:
        The data after processing.
    """
    data_to_process = data
    for key in keys:
        data_to_process = data_to_process[key]

    new_data = change_timestamp_format(data_to_process)
    values_in_range = filter_values_by_interval(new_data, interval)

    # Update the nested part of the data with the processed data
    nested_data = data
    for key in keys[:-1]:
        nested_data = nested_data[key]

    nested_data[keys[-1]] = new_data

    return values_in_range

def get_chain_id_by_name(chain_name:str):
    """
    Intent: Retrieve the ID of a chain based on its name from an API that provides a list of chains and their IDs from Centic API.

    Inputs:
        chain_name: The name of the chain_name for which the ID is to be retrieved.

    Outputs:
        The ID of the specified chain_name if found, or None if the chain_name name is not in the list.
    """
    # Call the API to retrieve the list of chain_name and IDs
    api_url = 'https://api-staging.centic.io/dev/v3/common/chains'
    response = requests.get(api_url, headers={'accept': '*/*'})
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    chains_data = response.json().get('chains', {})
    for chain_id, chain_info in chains_data.items():
        if chain_info.get('name') == chain_name:
            return chain_id
    # Handle the case when the chain_name name is not found
    print(f"chain_name '{chain_name}' not found in the list.")
    return None
