import os

from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import redirect
from access import login_permission_required
from dbcon import work_with_db, make_update
from sql_provider import SQLProvider
from blueprint.scenario_pay.utils import add_to_basket, clear_basket

pay_app = Blueprint('pay', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@pay_app.route('/choose_clientpay', methods=['GET', 'POST'])
@login_permission_required
def choose_client():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('client_name.sql'))
        return render_template('choose_client.html', res=items,
                               name=['Покупатель', 'Город', 'Телефон', 'Дата контракта', 'Накопленная сумма', ''])
    db_config = current_app.config['DB_CONFIG']
    sql3 = provider.get('stat3.sql')
    result3 = make_update(db_config, sql3)
    c_id = request.form.get('c_id')
    session["c_id"] = c_id
    print(c_id)
    return redirect('/pay/')


@pay_app.route('/', methods=['POST', 'GET'])
@login_permission_required
def basket():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        c_id = session.get("c_id", None)
        if not c_id:
            return redirect('/pay/choose_clientpay')
        current_basket = session.get('basket', [])
        print(current_basket)
        sql = provider.get('order_list.sql', c_id=c_id)
        result = work_with_db(config=db_config, sql=sql)
        sql1 = provider.get('name.sql', c_id=c_id)
        result1 = work_with_db(config=db_config, sql=sql1)
        return render_template('basket_order_listp.html', items=result, basket=current_basket, c_name=result1)
    else:
        ord_id = request.form.get('ord_id', None)
        sql = provider.get('order_item.sql', id=ord_id)
        items = work_with_db(config=db_config, sql=sql)
        if not items:
            return ''
        add_to_basket(items[0])
        return redirect('/pay')


@pay_app.route('/clearpay', methods=['POST', 'GET'])
def clear_basket_handler():
    clear_basket()
    return redirect('/pay')


@pay_app.route('/buytopay', methods=["GET", "POST"])
def buy_items():
    db_config = current_app.config['DB_CONFIG']
    basket = session.get('basket', [])
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        sql1 = provider.get('name.sql', c_id=session.get('c_id'))
        result1 = work_with_db(config=db_config, sql=sql1)
        return render_template('input_clientpay.html', basket=current_basket, c_name=result1)
    else:
        for item in basket:

            sql4 = provider.get('update_count.sql', **item)
            sql5 = provider.get('update_date.sql', **item)
            # sql6 = provider.get('update_customer.sql', **item)
            sql2 = provider.get('stat2.sql', **item)
            # print(sql6)
            result4 = make_update(db_config, sql4)
            result5 = make_update(db_config, sql5)
            # result6 = make_update(db_config, sql6)
            result2 = make_update(db_config, sql2)

            if not result2:
                return ""
            if not result4:
                return ""
            if not result5:
                return ""
            # if not result6:
            #     return ""
        clear_basket()
        session.pop('c_id')

        return redirect('/')
