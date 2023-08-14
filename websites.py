from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
import main as logic
from forms import RegistrationForm
import secrets
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy.orm import Session
from instance import DatabaseM as Table_manager
import git

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
UserName = None
Items = []
secret_token = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

<<<<<<< HEAD

=======
>>>>>>> 5ef27cc369a62597d8c76fc567bb8ad5bfe0a2a7

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
<<<<<<< HEAD
      db.create_all()
      db.session.commit()
=======
    db.create_all()
    db.session.commit()


DATABASE_PATH = 'instance/site.db'

table_manager = Table_manager.NewTableManager(DATABASE_PATH)
>>>>>>> 5ef27cc369a62597d8c76fc567bb8ad5bfe0a2a7


DATABASE_PATH = 'Seo_web2/instance/site.db'
table_manager = Table_manager.NewTableManager(DATABASE_PATH)

@app.route("/")
@app.route("/home")
def home():
    global UserName, Items
    UserName = None
    Items = []
    return render_template('home.html')



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
    return render_template('tables.html', datas=ohlc_data)



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



@app.route("/userhome")
def userhome():
    global Items
    global UserName
    if UserName == None:
        return redirect("login")
    else:
        logic.user_home_imp(UserName, Items, table_manager)
    return render_template('Userlayout.html', UserName=UserName, item=Items)



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


@app.route("/update_server", methods=['GET','POST'])
def webhook():
    repo = git.Repo('C:\Seo_web\Seo_web2')
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully', 200

<<<<<<< HEAD

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
=======
    
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
    
>>>>>>> 5ef27cc369a62597d8c76fc567bb8ad5bfe0a2a7
