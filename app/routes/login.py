from flask import Blueprint, render_template, request, redirect, url_for
from services import create_connection, execute_query, fetch_query

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = create_connection()
        print(connection)
        return redirect(url_for('home'))
    return render_template('login.html')