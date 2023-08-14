import unittest
import sqlite3
from instance import DatabaseM


TEST_DATABASE_NAME = 'instance/site.db'
NewTableManager=DatabaseM.NewTableManager(TEST_DATABASE_NAME)
class TestNewTableManager(unittest.TestCase):
    def setUp(self):
        self.new_table_manager = DatabaseM.NewTableManager(TEST_DATABASE_NAME)
        self.new_table_manager.connect()

    def tearDown(self):
        self.new_table_manager.disconnect()

    def test_insert_user_currency_data(self):
        userid = 1
        currencyid = 2
        timeid = 1

        self.new_table_manager.insert_user_currency_data(userid, currencyid, timeid)

        data = self.new_table_manager.fetch_user_currency_data()
        self.assertEqual(data[0], (userid, currencyid, timeid))

    def test_get_user_id(self):
        # Assuming you have previously inserted a user with username "Amosh"
        user = "Amosh"
        expected_id = 1

        user_id = self.new_table_manager.get_user_id(user)

        self.assertEqual(user_id, expected_id)

    def test_get_currency_id(self):
        # Assuming you have previously inserted a currency with currencypair "AUDUSD"
        currency = "AUDUSD"
        expected_id = 1

        currency_id = self.new_table_manager.get_curency_id(currency)

        self.assertEqual(currency_id, expected_id)

    def test_get_time_id(self):
        # Assuming you have previously inserted a timeframe with time "Daily"
        time = "Daily"
        expected_id = 1

        time_id = self.new_table_manager.get_time_id(time)

        self.assertEqual(time_id, expected_id)

    def test_check_history(self):
        # Assuming you have previously inserted some user_currency data
        # with userid = 1, currencyid = 2, and timeid = 1
        userid = 1

        history = self.new_table_manager.check_history(userid)

        self.assertIsNotNone(history)

    def test_get_timebyid(self):
        # Assuming you have previously inserted a timeframe with time "Daily" and id = 1
        timeid = 1
        expected_time = "Daily"

        time = self.new_table_manager.get_timebyid(timeid)

        self.assertEqual(time[0], expected_time)

    def test_get_currencybyid(self):
        # Assuming you have previously inserted a currency with currencypair "AUDUSD" and id = 1
        currencyid = 1
        expected_currency = "AUDUSD"

        currency = self.new_table_manager.get_currencybyid(currencyid)

        self.assertEqual(currency[0], expected_currency)

    def test_check_user_history(self):
        # Assuming you have previously inserted some user_currency data
        # with userid = 1, currencyid = 2, and timeid = 1
        userid = 1
        currencyid = 2
        timeid = 1

        result = self.new_table_manager.check_user_history((userid, currencyid, timeid))

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
