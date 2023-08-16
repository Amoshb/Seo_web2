""""
This file contains the flask server where webpages are being routed to specific paths
"""

# Import required modules and libraries
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
import main as logic
from forms import RegistrationForm
import secrets
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy.orm import Session
import DatabaseM as Table_manager
import git


# Initialize the Flask app
app = Flask(__name__)
proxied = FlaskBehindProxy(app)


# Initialize global variables
UserName = None
Items = []
secret_token = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_token


# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Define the User model for the database
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"
  

# Create database tables
with app.app_context():
    db.create_all()
    db.session.commit()


DATABASE_PATH = 'Seo_web2/instance/site.db'
table_manager = Table_manager.NewTableManager(DATABASE_PATH)


# Initialize paths and route functions
# Home page
@app.route("/")
@app.route("/home")
def home():
    global UserName, Items
    UserName = None
    Items = []
    return render_template('home.html')


# Table page
@app.route("/tables", methods=['GET', 'POST'])
def table_page():
    ohlc_data = None
    msg = None
    if request.method == "POST":
        selected_CP = request.form.get("Currency_Pairs")
        selected_T = request.form.get("Time_Frame")
        try:
            ohlc_data, msg = logic.get_table_data(selected_CP, selected_T)
        except Exception as e:
            msg = f"An error occurred: {str(e)}"

    if ohlc_data == None:
        return render_template('tables.html', msg=msg)
    else:
        msg = selected_CP + " " + selected_T
        return render_template('tables.html', datas=ohlc_data, msg=msg)


# Currency page
@app.route("/currency", methods=['GET', 'POST'])
def second_page():
    chart_json = None
    if request.method == "POST":
        selected_CP = request.form.get("Currency_Pairs")
        selected_T = request.form.get("Time_Frame")
        try:
            chart_json, msg = logic.get_chart_data(selected_CP, selected_T)
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
            return render_template('currency.html', msg=msg)

        if chart_json == None:
            return render_template('currency.html', msg=msg)

    return render_template('currency.html', chart_json=chart_json)


# User registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        try:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login')) # if so - send to login page
        except Exception as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            flash(f'An error occurred while creating the account: {str(e)}', 'error')
            return render_template('register.html', title='Register', form=form)

    return render_template('register.html', title='Register', form=form)


# User login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    global UserName
    form = RegistrationForm()
    if request.method == 'POST':
        user = User(username=form.username.data, password=form.password.data)
        try:
            user_info = logic.handle_login(user)
            if user_info is False:
                flash('Invalid username or password. Please try again.', 'error')
            else:
                UserName = user.username
                return redirect(url_for("userhome"))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('login.html', title='Login', form=form)

    return render_template('login.html', title='Login', form=form)


# User home page
@app.route("/userhome")
def userhome():
    global Items
    global UserName
    if UserName == None:
        return redirect("login")
    else:
        logic.user_home_imp(UserName, Items, table_manager)
    return render_template('Userlayout.html', UserName=UserName, item=Items)


# User chart page
@app.route("/userchart", methods=['GET', 'POST'])
def userchart():
    global UserName, Items
    if UserName is None:
        return redirect("login")
    try:
        if request.method == "POST":
            selected_CP = request.form["currency"]
            selected_CP, selected_T = selected_CP.split(" ")
            chart_json, msg = logic.get_chart_data(selected_CP, selected_T)
            return render_template('userchart.html', chart_json=chart_json, item=Items, UserName=UserName, msg=msg)
    except Exception as e:
        msg = f"An error occurred: {str(e)}"
        return render_template('userchart.html', msg=msg)

    return render_template('userchart.html', UserName=UserName, item=Items)


# User currency page
@app.route("/usercurrency", methods=['GET', 'POST'])
def usercurrency():
    global Items, UserName
    if UserName is None:
        return redirect("login")

    Items = logic.get_items(logic.get_user_id_from_username(UserName,table_manager), table_manager)

    msg = None
    redirec = False
    if request.method == "POST":
        selected_CP = request.form.get("Currency_Pairs")
        selected_T = request.form.get("Time_Frame")
        try:
            if logic.insert_user_currency_data(UserName, selected_CP, selected_T, table_manager):
                redirec = True
            else:
                msg = "Already taken"
        except Exception as e:
            msg = msg = f"An error occurred: {str(e)}"

    if redirec:
        return redirect('userhome')

    return render_template('usercurrency.html', UserName=UserName, item=Items, msg=msg)


# Webhook for updating the server
@app.route("/update_server", methods=['GET','POST'])
def webhook():
    repo = git.Repo('/home/Amoshb/mysite/Seo_web2')
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully', 200


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")

