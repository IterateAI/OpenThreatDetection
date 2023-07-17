from flask import Blueprint, render_template
from datetime import datetime
 
test_bp = Blueprint('test_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets')

@test_bp.route('/t1')
def t1_page():
    now = datetime.now()
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f'<h1>WEPWEB Test Page, we are in deep now: {dt_string}</h1>'

@test_bp.route('/')
def test_page():
    return render_template("test/test.html")