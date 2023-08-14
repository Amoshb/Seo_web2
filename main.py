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


def get_database_data(db_path, sql):
    if db_path == None or db_path == "" or sql == None or sql == "":
        print("Your path or sql query is None.")
        return None

    engine = db.create_engine(db_path)
    with engine.connect() as connection:
        query_result = connection.execute(db.text(sql)).fetchall()
    return query_result

def check_user_credentials(username, password, db_path):
    if db_path is None or db_path == "":
        print("Your path is None.")
        return None

    engine = db.create_engine(db_path)
    with engine.connect() as connection:
        query = db.text('SELECT * FROM user WHERE username=:username AND password=:password')
        query_result = connection.execute(query, {"username": username, "password": password}).fetchone()

    return query_result is not None




def get_table_data(selected_CP, selected_T):
    if selected_CP == "" or selected_T == ""or selected_CP == None or selected_T == None:
        return None, "Select both options!"
    else:
        table = selected_CP + selected_T
        queries = f"SELECT date, open, high, low, close FROM {table};"
        get_db_path = 'sqlite:///Seo_web2/forex_data2.db'
        ohlc_data = get_database_data(get_db_path, queries)
        return ohlc_data, None


def get_chart_data(selected_CP, selected_T):
    if selected_CP == "" or selected_T == "" or selected_CP == None or selected_T == None:
        return None, "Select options!"
    else:
        table = selected_CP + selected_T
        queries = f"SELECT date, open, high, low, close FROM {table};"
        get_db_path = 'sqlite:///Seo_web2/forex_data2.db'
        ohlc_data = get_database_data(get_db_path, queries)
        df = pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
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
        return chart_json, None


def handle_login(user):
    if user == None or user == "":
        return None
        
    get_db_path = 'sqlite:///Seo_web2/instance/site.db'
    user_info = check_user_credentials(user.username, user.password, get_db_path)
    return user_info

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




def get_user_id_from_username(username, table_manager):
    table_manager.connect()
    user_id = table_manager.get_user_id(username)
    table_manager.disconnect()
    return user_id

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


