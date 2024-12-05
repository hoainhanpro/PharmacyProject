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
        res = execute_query(connection, procedure='LoginUser', params=(username, hash_password, password))
        if res and res[0][0] == 'Login failed':
            flash('Đăng nhập thất bại')
            return redirect(url_for('login.login'))
        
        if res[0][1] == 'khachhang':
            user = execute_query(connection, f'SELECT * FROM khachhang WHERE email = "{username}"')
        else:
            user = execute_query(connection, f'SELECT * FROM nhanvien WHERE email = "{username}"')
        session['role'] = res[0][1]
        session['user'] = user[0]
        if session['role'] == 'khachhang':
            return redirect(url_for('homepage.homepage'))
        elif session['role'] == 'QUANLY':
            return redirect(url_for('medicinemanager.medicinemanager'))
        elif session['role'] == 'NHANVIENGIAOHANG':
            return redirect(url_for('receiptmanager.danh_sach_hoa_don'))
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage.homepage'))