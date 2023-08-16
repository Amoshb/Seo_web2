"""
This file contains a class helps to manipulate the data from the database eg. insert, select, etc
"""

import sqlite3

class NewTableManager:
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def insert_user_currency_data(self, userid, currencyid, timeid):
        insert_query = '''
            INSERT INTO user_currency (userid, currencyid, timeid)
            VALUES (?, ?, ?)
        '''
        self.cursor.execute(insert_query, (userid, currencyid, timeid))
        self.conn.commit()
    
    def fetch_user_currency_data(self):
        select_query = '''
            SELECT userid, currencyid, timeid
            FROM user_currency
        '''
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def insert_currency(self, currencypair):
        insert_query = '''
            INSERT INTO currency (currencypair)
            VALUES (?)
        '''
        self.cursor.execute(insert_query, (currencypair))
        self.conn.commit()
    
    def fetch_currency_data(self):
        select_query = '''
            SELECT *
            FROM currency
        '''
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def get_user_id(self, user):
        select_query = '''
            SELECT id 
            FROM user
            WHERE username = ?
        '''
        self.cursor.execute(select_query, (user,))
        result = self.cursor.fetchone()
        print(user, result)

        if result:
            return result[0] 
        else:
            return None 
        
    def get_curency_id(self, currency):
        select_query = '''
            SELECT id 
            FROM currency
            WHERE currencypair = ?
        '''
        self.cursor.execute(select_query, (currency,))
        result = self.cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None 
        
    def get_time_id(self, time):
        select_query = '''
            SELECT id 
            FROM timeframe
            WHERE time = ?
        '''
        self.cursor.execute(select_query, (time,))
        result = self.cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None 
        
    def check_history(self, Userid):
        select_query = '''
            SELECT currencyid, timeid
            FROM user_currency
            WHERE userid = ?
        '''
        self.cursor.execute(select_query, (Userid,))
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return None

    def get_timebyid(self, timeid):
        select_query = '''
            SELECT time
            FROM timeframe
            WHERE id = ?
        '''
        self.cursor.execute(select_query, (timeid,))
        result = self.cursor.fetchone()
        return result
    
    def get_currencybyid(self, currnecyid):
        select_query = '''
            SELECT currencypair
            FROM currency
            WHERE id = ?
        '''
        self.cursor.execute(select_query, (currnecyid,))
        result = self.cursor.fetchone()
        return result

    def check_user_history(self, tuple):
        select_query = '''
            SELECT userid, currencyid, timeid
            FROM user_currency
        '''
        self.cursor.execute(select_query)
        result = self.cursor.fetchall()
        if tuple in result:
            return True
        else:
            return False

import unittest
import sqlite3
#from instance import DatabaseM


TEST_DATABASE_NAME = 'instance/site.db'
#NewTableManager=NewTableManager(TEST_DATABASE_NAME)
class TestNewTableManager(unittest.TestCase):
    def setUp(self):
        self.new_table_manager = NewTableManager(TEST_DATABASE_NAME)
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
