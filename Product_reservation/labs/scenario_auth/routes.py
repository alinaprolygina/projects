from flask import Blueprint, render_template, session, request, current_app
from sql_provider import SQLProvider
from dbcon import get_db_config, work_with_db
import os

auth_app = Blueprint('auth_app', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        sql = provider.get('auth.sql', log=login, pas=password)
        name_group = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not name_group:
            return render_template("index3.html")
        session['group_name'] = name_group[0]['user_group']
        print(session['group_name'])
        return render_template("menu.html")
