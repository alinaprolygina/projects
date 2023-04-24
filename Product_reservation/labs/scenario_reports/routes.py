from flask import Blueprint, render_template, request
from sql_provider import SQLProvider
from access import login_permission_required
from dbcon import get_db_config, work_with_db
import os

reports = Blueprint('reports', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@reports.route('/', methods=['GET', 'POST'])
@login_permission_required
def report_page():
    if request.method == 'GET':
        return render_template("report_menu.html")
