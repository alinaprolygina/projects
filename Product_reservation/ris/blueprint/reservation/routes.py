from flask import Blueprint, render_template, request

from access import login_permission_required, login_required
from dbcon import get_db_config, work_with_db
from sql_provider import SQLProvider

app_sql = Blueprint('reservation', __name__, template_folder='templates')
provider_hard = SQLProvider('C:/Users/526/Desktop/BMSTU/5 sem/RIS/kursovaya/blueprint/reservation/sql')


@app_sql.route("/")
@login_required
def query_list():
    return render_template('menu_for_sql.html')


@app_sql.route('/sql1', methods=['GET', 'POST'])
@login_permission_required
def sql1():
    if request.method == 'GET':
        return render_template('input_name.html')
    else:
        name = request.form.get('name')
        db_config = get_db_config()

        if name != "":
            sql = provider_hard.get('1.sql', name=name, month=4, year=2013)
            result = work_with_db(config=db_config, sql=sql)
            if not result:
                stroka = ['Таких записей нет.']
                res_keys = 0
            else:
                stroka = result
                res_keys = result[0].keys()
        else:
            stroka = ['Пустой ввод.']
            res_keys = 0

        keyList = ['Номер заказа', 'Название товара', 'Имя покупателя']
        context = {'itemList': stroka, 'keys': res_keys, 'k_list': keyList}
        return render_template('result1.html', **context)


@app_sql.route('/sql2', methods=['GET', 'POST'])
@login_permission_required
def sql2():
    if request.method == 'GET':
        return render_template('input_material.html')
    else:
        material = request.form.get('material')
        db_config = get_db_config()

        if material != "":
            sql = provider_hard.get('2.sql', material=material)
            result = work_with_db(config=db_config, sql=sql)
            if not result:
                stroka = ['Таких записей нет.']
                res_keys = 0
            else:
                stroka = result
                res_keys = result[0].keys()
        else:
            stroka = ['Пустой ввод.']
            res_keys = 0

        keyList = ['Название товара']
        context = {'itemList': stroka, 'keys': res_keys, 'k_list': keyList}
        return render_template('result2.html', **context)


@app_sql.route('/sql3', methods=['GET', 'POST'])
@login_permission_required
def sql3():
    if request.method == 'GET':
        return render_template('input_date.html')
    else:
        month = request.form.get('month')
        year = request.form.get('year')
        db_config = get_db_config()

        if month != "" and year != "":
            sql = provider_hard.get('3.sql', month=month, year=year)
            result = work_with_db(config=db_config, sql=sql)
            if not result:
                stroka = ['Таких записей нет.']
                res_keys = 0
            else:
                stroka = result
                res_keys = result[0].keys()
        else:
            stroka = ['Пустой ввод.']
            res_keys = 0

        keyList = ['Номер покупателя', 'Имя покупателя', 'Город', 'Телефон', 'Дата контракта', 'Накопленная сумма']
        context = {'itemList': stroka, 'keys': res_keys, 'k_list': keyList}
        return render_template('result3.html', **context)

