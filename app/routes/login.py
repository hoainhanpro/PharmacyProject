import hashlib
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from services import create_connection, execute_query

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hash_password = hashlib.sha256(password.encode()).hexdigest()
        connection = create_connection()
        res = execute_query(connection, procedure='LoginKhachHang', params=(username, hash_password))
        if res and res[0][0] == 'Login failed':
            flash('Đăng nhập thất bại')
            return redirect(url_for('login.login'))
        
        session['username'] = username
        return redirect(url_for('homepage.homepage'))
    return render_template('login.html')