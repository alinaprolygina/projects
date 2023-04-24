from flask import Blueprint, render_template, current_app, request
from werkzeug.utils import redirect

from sql_provider import SQLProvider
from dbcon import change_db, work_with_db
import os
from access import login_permission_required


change_tables = Blueprint('change_tables', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@change_tables.route('/', methods=['GET', 'POST'])
@login_permission_required
def change_index():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_select.sql'))
        print(items)
        return render_template('change_menu.html', res=items, name=[ 'Покупатель', 'Дата заказа', 'Стоимость'])
    else:
        order_id = request.form.get('order_id')
        sql = provider.get('sql_delete_1.sql', order_id=order_id)
        key = change_db(current_app.config['DB_CONFIG'], sql)
        if key:
            return redirect('/redact')

        return 'Error input'


@change_tables.route('/sql_change_1', methods=['GET', 'POST'])
@login_permission_required
def change_tests():
    if request.method == 'GET':
        return render_template('sql_change_1.html')
    else:
        value1 = request.form.get('value1', None)
        value2 = request.form.get('value2', None)
        value3 = request.form.get('value3', None)
        # value4 = request.form.get('value4', None)
        if value1 and value2 and value3:
            sql = provider.get('sql_change_1.sql', gener1=value1, gener2=value2, gener3=value3)
            if not change_db(current_app.config['DB_CONFIG'], sql):
                return 'Error input'
            return redirect('/redact')
        else:
            return 'Not found value'


@change_tables.route('/sql_update_1', methods=['GET', 'POST'])
@login_permission_required
def update_tests():
    if request.method == 'GET':
        return render_template('sql_update_1.html')
    else:
        value1 = request.form.get('value1', None)
        value2 = request.form.get('value2', None)
        value3 = request.form.get('value3', None)
        value4 = request.form.get('value4', None)
        if value1 and value2 and value3 and value4:
            sql = provider.get('sql_update_1.sql', gener1=value1, gener2=value2, gener3=value3, gener4=value4 )
            if not change_db(current_app.config['DB_CONFIG'], sql):
                return 'Error input'
            return redirect('/redact')
        else:
            return 'Not found value'

