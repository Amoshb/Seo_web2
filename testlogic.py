# test_logic.py
import unittest
from main import *
import sqlalchemy as db
from unittest.mock import Mock
import DatabaseM as Table_manager

class TestLogicFunctions(unittest.TestCase):
    def test_valid_inputs(self):
        # Test case: Valid database path and SQL query
        db_path = 'sqlite:///instance//site.db'
        sql = 'SELECT id, username FROM user;'
        result = get_database_data(db_path, sql)
        expected_result = [(1, 'Amosh'), (2, 'Jenny'), (3, 'Roxxy')]
        self.assertEqual(result, expected_result)

    def test_empty_db_path(self):
        # Test case: Empty database path
        db_path = ''
        sql = 'SELECT * FROM users;'
        result = get_database_data(db_path, sql)
        self.assertIsNone(result)

    def test_empty_sql_query(self):
        # Test case: Empty SQL query
        db_path = 'sqlite:///instance//site.db'
        sql = ''
        result = get_database_data(db_path, sql)
        self.assertIsNone(result)

    def test_none_db_path(self):
        # Test case: None database path
        db_path = None
        sql = 'SELECT * FROM users;'
        result = get_database_data(db_path, sql)
        self.assertIsNone(result)

    def test_none_sql_query(self):
        # Test case: None SQL query
        db_path = 'sqlite:///instance//site.db'
        sql = None
        result = get_database_data(db_path, sql)
        self.assertIsNone(result)




    def test_valid_credentials(self):
        # Test case: Valid username and password
        db_path ='sqlite:///instance//site.db'
        username = 'Amosh'
        password = 'Inazuma@12'
        result = check_user_credentials(username, password, db_path)
        self.assertTrue(result)

    def test_empty_db_path(self):
        # Test case: Empty database path
        db_path = ''
        username = 'Amosh'
        password = 'Inazuma@12'
        result = check_user_credentials(username, password, db_path)
        self.assertIsNone(result)

    def test_none_db_path(self):
        # Test case: None database path
        db_path = None
        username = 'Amosh'
        password = 'Inazuma@12'
        result = check_user_credentials(username, password, db_path)
        self.assertIsNone(result)





    def test_valid_options(self):
        # Test case: Valid selected currency pair and time frame
        selected_CP = "EURUSD"
        selected_T = "Daily"

        # Assuming we have valid data for the selected currency pair and time frame
        ohlc_data, msg = get_table_data(selected_CP, selected_T)

        self.assertIsNotNone(ohlc_data)
        self.assertIsNone(msg)

    def test_empty_selected_CP(self):
        # Test case: Empty selected currency pair
        selected_CP = ""
        selected_T = "Daily"

        ohlc_data, msg = get_table_data(selected_CP, selected_T)

        self.assertIsNone(ohlc_data)
        self.assertEqual(msg, "Select both options!")

    def test_empty_selected_T(self):
        # Test case: Empty selected time frame
        selected_CP = "EURUSD"
        selected_T = ""

        ohlc_data, msg = get_table_data(selected_CP, selected_T)

        self.assertIsNone(ohlc_data)
        self.assertEqual(msg, "Select both options!")

    def test_none_selected_CP(self):
        # Test case: None selected currency pair
        selected_CP = None
        selected_T = "Daily"

        ohlc_data, msg = get_table_data(selected_CP, selected_T)

        self.assertIsNone(ohlc_data)
        self.assertEqual(msg, "Select both options!")

    def test_none_selected_T(self):
        # Test case: None selected time frame
        selected_CP = "EURUSD"
        selected_T = None

        ohlc_data, msg = get_table_data(selected_CP, selected_T)

        self.assertIsNone(ohlc_data)
        self.assertEqual(msg, "Select both options!")





    def test_valid_options(self):
        # Test case: Valid selected currency pair and time frame
        selected_CP = "EURUSD"
        selected_T = "Daily"

        # Assuming we have valid data for the selected currency pair and time frame
        chart_json, msg = get_chart_data(selected_CP, selected_T)

        self.assertIsNotNone(chart_json)
        self.assertIsNone(msg)

    def test_empty_selected_CP(self):
        # Test case: Empty selected currency pair
        selected_CP = ""
        selected_T = "Daily"

        chart_json, msg = get_chart_data(selected_CP, selected_T)

        self.assertIsNone(chart_json)
        self.assertEqual(msg, "Select options!")

    def test_empty_selected_T(self):
        # Test case: Empty selected time frame
        selected_CP = "EURUSD"
        selected_T = ""

        chart_json, msg = get_chart_data(selected_CP, selected_T)

        self.assertIsNone(chart_json)
        self.assertEqual(msg, "Select options!")

    def test_none_selected_CP(self):
        # Test case: None selected currency pair
        selected_CP = None
        selected_T = "Daily"

        chart_json, msg = get_chart_data(selected_CP, selected_T)

        self.assertIsNone(chart_json)
        self.assertEqual(msg, "Select options!")

    def test_none_selected_T(self):
        # Test case: None selected time frame
        selected_CP = "EURUSD"
        selected_T = None

        chart_json, msg = get_chart_data(selected_CP, selected_T)

        self.assertIsNone(chart_json)
        self.assertEqual(msg, "Select options!")



        
class TestHandleLogin(unittest.TestCase):

    def test_valid_credentials(self):
        # Create a mock user object with valid credentials
        class MockUser:
            def __init__(self, username, password):
                self.username = username
                self.password = password

        mock_user = MockUser("Amosh", "Inazuma@12")

        # Call the handle_login function
        user_info = handle_login(mock_user)

        # Check that the user_info is not None (valid credentials)
        self.assertIsNotNone(user_info)

    def test_invalid_credentials(self):
        # Create a mock user object with invalid credentials
        class MockUser:
            def __init__(self, username, password):
                self.username = username
                self.password = password

        mock_user = MockUser("invalid_username", "invalid_password")

        # Call the handle_login function
        user_info = handle_login(mock_user)

        # Check that the user_info is None (invalid credentials)
        self.assertFalse(user_info)

    def test_empty_user(self):
        # Call the handle_login function with an empty user object
        user_info = handle_login(None)

        # Check that the user_info is None
        self.assertIsNone(user_info)

    def test_user_home_imp(self):
        # Write test cases for user_home_imp function
        pass



class TestGetUserIDFromUsername(unittest.TestCase):

    def test_valid_username(self):
        # Create a mock table_manager with a get_user_id method
        mock_table_manager = Mock()
        mock_table_manager.get_user_id.return_value = 1  # Return a user ID

        # Call the get_user_id_from_username function
        user_id = get_user_id_from_username("Amosh", mock_table_manager)

        # Check that the user_id matches the expected value
        self.assertEqual(user_id, 1)

    def test_invalid_username(self):
        # Create a mock table_manager with a get_user_id method
        mock_table_manager = Mock()
        mock_table_manager.get_user_id.return_value = None  # Return None for invalid username

        # Call the get_user_id_from_username function
        user_id = get_user_id_from_username("invalid_username", mock_table_manager)

        # Check that the user_id is None for invalid username
        self.assertIsNone(user_id)


class TestGetItems(unittest.TestCase):

    def test_items_found(self):
        DATABASE_PATH = 'instance/site.db'
        table_manager = Table_manager.NewTableManager(DATABASE_PATH)
        user = 1

        # Call the get_items function
        items = get_items(user, table_manager)

        # Check that the items match the expected result
        self.assertIsNotNone(items)

    def test_no_items(self):
        # Create a mock table_manager with appropriate methods
        mock_table_manager = Mock()
        mock_table_manager.check_history.return_value = None  # Simulate no items found

        # Call the get_items function
        items = get_items(1, mock_table_manager)

        # Check that the items list is empty when no items are found
        self.assertEqual(items, [])

    def test_user_id_none(self):
        # Call the get_items function with user_id as None
        items = get_items(None, Mock())  # We don't need a mock table_manager for this test

        # Check that the result is None when user_id is None
        self.assertEqual(items, [])


    def test_insert_user_currency_data(self):
        # Write test cases for insert_user_currency_data function
        pass

if __name__ == '__main__':
    unittest.main()
