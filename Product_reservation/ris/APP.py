from flask import Flask, render_template, session
from blueprint.reservation.routes import app_sql
from sql_provider import SQLProvider
from blueprint.scenario_auth.routes import auth_app
from blueprint.scenario_basket.routes import basket_app
from blueprint.scenario_pay.routes import pay_app
import json

app = Flask(__name__)

app.config['DB_CONFIG'] = json.load(open('configs/config.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['SECRET_KEY'] = 'super secret key'
provider = SQLProvider('blueprint/reservation/sql')
app.register_blueprint(app_sql, url_prefix='/Reserv')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')
app.register_blueprint(pay_app, url_prefix='/pay')


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/exit')
def clear_session():
    session.clear()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5008)
