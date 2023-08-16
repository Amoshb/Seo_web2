""""
This file contains the logic parts for the website.py file 
"""

import json
from flask import Flask, render_template, url_for, flash, redirect, request
import plotly
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Function to retrieve data from the database
def get_database_data(db_path, sql):
    # Check if path or SQL query is None
    if db_path == None or db_path == "" or sql == None or sql == "":
        print("Your path or sql query is None.")
        return None

    engine = db.create_engine(db_path)
    with engine.connect() as connection:
        query_result = connection.execute(db.text(sql)).fetchall()
    return query_result


# Function to check user credentials
def check_user_credentials(username, password, db_path):
    # Check if path is None
    if db_path is None or db_path == "":
        print("Your path is None.")
        return None

    engine = db.create_engine(db_path)
    with engine.connect() as connection:
        query = db.text('SELECT * FROM user WHERE username=:username AND password=:password')
        query_result = connection.execute(query, {"username": username, "password": password}).fetchone()

    return query_result is not None


# Function to get table data
def get_table_data(selected_CP, selected_T):
    # Check if options are selected
    if selected_CP == "" or selected_T == ""or selected_CP == None or selected_T == None:
        return None, "Select both options!"
    else:
        table = selected_CP + selected_T
        queries = f"SELECT date, open, high, low, close FROM {table};"
        get_db_path = 'sqlite:///Seo_web2/forex_data2.db'
        ohlc_data = get_database_data(get_db_path, queries)
        return ohlc_data, None


# Function to generate and set chart data
def set_chart(dataframe, selected_CP, selected_T):
    # Processing data and creating chart traces
    df = dataframe
    df['SMA4'] = df['Close'].rolling(window=2).mean()
    df['SMA8'] = df['Close'].rolling(window=4).mean()
    df['SMA12'] = df['Close'].rolling(window=8).mean()

    candlestick_trace = go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlesticks',
    )

    sma4_trace = go.Scatter(
        x=df['Date'],
        y=df['SMA4'],
        mode='lines',
        name='SMA 4',
        visible='legendonly',
        legendgroup='SMA',
    )

    sma8_trace = go.Scatter(
        x=df['Date'],
        y=df['SMA8'],
        mode='lines',
        name='SMA 8',
        visible='legendonly',
        legendgroup='SMA',
    )

    sma12_trace = go.Scatter(
        x=df['Date'],
        y=df['SMA12'],
        mode='lines',
        name='SMA 12',
        visible='legendonly',
        legendgroup='SMA',
    )

    # Creating and configuring the chart figure
    fig = go.Figure(data=[candlestick_trace])
    fig.add_trace(candlestick_trace)
    fig.add_trace(sma4_trace)
    fig.add_trace(sma8_trace)
    fig.add_trace(sma12_trace)
    fig.update_layout(
        title=f'Forex Candlestick Chart {selected_CP} ({selected_T})',
        xaxis_title='Date',
        yaxis_title='Price',
    )
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return chart_json
    

# Function to get chart data
def get_chart_data(selected_CP, selected_T):
    # Check if options are selected
    if selected_CP == "" or selected_T == "" or selected_CP == None or selected_T == None:
        return None, "Select options!"
    else:
        table = selected_CP + selected_T
        queries = f"SELECT date, open, high, low, close FROM {table};"
        get_db_path = 'sqlite:///Seo_web2/forex_data2.db'
        ohlc_data = get_database_data(get_db_path, queries)
        dataframe =pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
        chart_json = set_chart(dataframe, selected_CP, selected_T)
        return chart_json, None
    

# Function to handle user login
def handle_login(user):
    if user == None or user == "":
        return None

    get_db_path = 'sqlite:///Seo_web2/instance/site.db'
    user_info = check_user_credentials(user.username, user.password, get_db_path)
    return user_info


# Function to handle user home page logic
def user_home_imp(UserName, item, table_manager):
    table_manager.connect()
    user_id = table_manager.get_user_id(UserName)
    itemid = table_manager.check_history(user_id)
    if itemid == None:
        pass
    else:
        for x, y in itemid:
            pairs = table_manager.get_currencybyid(x) + table_manager.get_timebyid(y)
            if pairs in item:
                pass
            else:
                item.append(pairs)
    table_manager.disconnect()


# Function to get user ID from username
def get_user_id_from_username(username, table_manager):
    table_manager.connect()
    user_id = table_manager.get_user_id(username)
    table_manager.disconnect()
    return user_id


# Function to get user's currency items
def get_items(user_id, table_manager):
    if user_id == None:
        return []
    items = []
    table_manager.connect()
    itemid = table_manager.check_history(user_id)
    if itemid is not None:
        for x, y in itemid:
            pairs = table_manager.get_currencybyid(x) + table_manager.get_timebyid(y)
            if pairs not in items:
                items.append(pairs)
    table_manager.disconnect()
    return items


# Function to insert user's selected currency data
def insert_user_currency_data(username, selected_CP, selected_T, table_manager):
    table_manager.connect()
    currencyid = table_manager.get_curency_id(selected_CP)
    timeid = table_manager.get_time_id(selected_T)
    userid = table_manager.get_user_id(username)
    print(userid)
    tup = (userid, currencyid, timeid)

    if not table_manager.check_user_history(tup):
        table_manager.insert_user_currency_data(userid, currencyid, timeid)
        table_manager.disconnect()
        return True
    else:
        table_manager.disconnect()
        return False


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
