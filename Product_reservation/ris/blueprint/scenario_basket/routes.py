import os

from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import redirect
from access import login_permission_required
from dbcon import work_with_db, make_update
from sql_provider import SQLProvider
from blueprint.scenario_basket.utils import add_to_basket, clear_basket

basket_app = Blueprint('basket', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/choose_client', methods=['GET', 'POST'])
@login_permission_required
def choose_client():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('client_name.sql'))
        return render_template('choose_client.html', res=items,
                               name=['Покупатель', 'Город', 'Телефон', 'Дата контракта', 'Накопленная сумма', ''])
    c_id = request.form.get('c_id')
    session["c_id"] = c_id
    print(c_id)
    return redirect('/basket/')


@basket_app.route('/', methods=['POST', 'GET'])
@login_permission_required
def basket():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        c_id = session.get("c_id", None)
        print(c_id)
        if not c_id:
            return redirect('/basket/choose_client')
        current_basket = session.get('basket', [])
        print(current_basket)
        sql = provider.get('order_list.sql')
        result = work_with_db(config=db_config, sql=sql)
        result = [[result[i], 1] for i in range(len(result))]
        sql1 = provider.get('name.sql', c_id=c_id)
        result1 = work_with_db(config=db_config, sql=sql1)
        return render_template('basket_order_list.html', items=result, basket=current_basket, c_name=result1[0])
    else:
        art_id = request.form.get('art_id', None)
        ordered_number = request.form.get('ordered_number', None)
        sql = provider.get('order_item.sql', id=art_id)
        items = work_with_db(config=db_config, sql=sql)
        if not items:
            return ''
        add_to_basket([items[0], ordered_number])
        return redirect('/basket')


@basket_app.route('/clear', methods=['POST', 'GET'])
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')


@basket_app.route('/buy', methods=["GET", "POST"])
def buy_items():
    db_config = current_app.config['DB_CONFIG']
    basket = session.get('basket', [])
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        sql1 = provider.get('name.sql', c_id=session.get('c_id'))
        result1 = work_with_db(config=db_config, sql=sql1)
        return render_template('input_client.html', basket=current_basket, c_name=result1[0])
    else:
        client_id = session.get('c_id')

        for item in basket:
            sql = provider.get('insert_item.sql', **item[0], count=item[1], client_id=client_id)
            sql1 = provider.get('update_article.sql', **item[0], count=item[1])
            result = make_update(db_config, sql)
            result1 = make_update(db_config, sql1)
            if not result:
                return ""
            if not result1:
                return ""
        clear_basket()
        session.pop('c_id')

        return redirect('/')
