
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

