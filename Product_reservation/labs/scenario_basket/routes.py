import datetime
import os

from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import redirect
from access import login_permission_required, login_required
from dbcon import get_db_config, work_with_db, make_update
from sql_provider import SQLProvider
from scenario_basket.utils import add_to_basket, clear_basket

basket_app = Blueprint('basket', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/', methods=['POST', 'GET'])
@login_permission_required
def basket():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        sql = provider.get('order_list.sql')
        result = work_with_db(config=db_config, sql=sql)
        return render_template('basket_order_list.html', items=result, basket=current_basket)
    else:
        service_id = request.form.get('service_id', None)
        sql = provider.get('order_item.sql', id=service_id)
        items = work_with_db(config=db_config, sql=sql)
        if not items:
            return ''

        add_to_basket(items[0])
        return redirect('/basket')


@basket_app.route('/clear', methods=['POST', 'GET'])
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')


@basket_app.route('/buy')
def buy_items():
    db_config = current_app.config['DB_CONFIG']
    basket = session.get('basket', [])

    for item in basket:
        sql = provider.get('insert_item.sql', **item)
        result = make_update(db_config, sql)
        if not result:
            return ""

        clear_basket()
    return redirect('/basket')
