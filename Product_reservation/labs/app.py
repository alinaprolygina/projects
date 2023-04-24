from flask import Flask, render_template, session
from blueprint_query import blueprint_query
from scenario_auth.routes import auth_app
from scenario_reports.routes import reports
from change_tables.routes import change_tables
from sql_provider import SQLProvider
from scenario_basket.routes import basket_app

import json


app = Flask(__name__)

app.config['DB_CONFIG'] = json.load(open('configs/config.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['basket'] = json.load(open('configs/permission_handler.json'))

provider = SQLProvider('blueprint_query/sql')

app.config['SECRET_KEY'] = 'super secret key'

app.register_blueprint(blueprint_query.query_bp, url_prefix='/zapros')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(reports, url_prefix='/reports')
app.register_blueprint(change_tables, url_prefix='/redact')
app.register_blueprint(basket_app, url_prefix='/basket')




@app.route('/')
def index():
    return render_template('menu.html')


@app.route('/exit')
def clear_session():
    session.clear()
    return render_template('menu.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5006)
