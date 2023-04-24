from flask import Blueprint, render_template, request, current_app
from sql_provider import SQLProvider
from dbcon import get_db_config, work_with_db
from access import login_permission_required, login_required
import os


query_bp = Blueprint('zapros', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query_bp.route('/')
@login_permission_required
def zaproses():
    return render_template("zaproses.html")


@query_bp.route('/input1')
@login_permission_required
def zaprose1_input():
    return render_template("zapros1_input.html")


@query_bp.route('/input2')
@login_permission_required
def zaprose2_input():
    return render_template("zapros2_input.html")


@query_bp.route('/output1', methods=["POST"])
@login_permission_required
def get_sql1():
    if request.method == 'POST':
        price = request.form.get('price')
    sql = provider.get('zap1.sql', price=price)
    print(sql)

    result = work_with_db(current_app.config['DB_CONFIG'], sql)
    if not result:
        return render_template("zapros1_output.html")
    return render_template("zapros1_output.html", items=result)


@query_bp.route('/output2', methods=["POST"])
@login_permission_required
def get_sql2():
    if request.method == 'POST':
        lang = request.form.get('lang')
    sql = provider.get('zap2.sql', lang=lang)
    result = work_with_db(current_app.config['DB_CONFIG'], sql)
    if not result:
        return render_template("zapros2_output.html")
    return render_template("zapros2_output.html", items=result)

