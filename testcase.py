import unittest
import api  
class TestAPIFunctions(unittest.TestCase):
    def test_portfolio_performance_success(self):
        wallet_address = "0xdc05090a39650026e6afe89b2e795fd57a3cfec7"
        interval = 6
        result = api.portfolio_performance(wallet_address, interval)
        self.assertIsNotNone(result)

    def test_portfolio_asset_success(self):
        wallet_address = "0xdc05090a39650026e6afe89b2e795fd57a3cfec7"
        interval = 6
        result = api.portfolio_asset(wallet_address, interval)
        self.assertIsNotNone(result)

    def test_portfolio_wallet_success(self):
        wallet_address = "0xdc05090a39650026e6afe89b2e795fd57a3cfec7"
        account_id = "0x1"
        result = api.portfolio_wallet(wallet_address, account_id)
        self.assertIsNotNone(result)
    def test_get_coin_history(self):
        coin_name = "ethereum"
        currency = "vnd"
        day =  6
        result = api.get_coin_history(coin_name, currency, day)
        self.assertIsNotNone(result)
if __name__ == '__main__':
    unittest.main()
