from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.database import create_connection, execute_query
import hashlib

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ho_va_ten = request.form['ho_va_ten']
        sdt = request.form['sdt']
        email = request.form['email']
        dia_chi = request.form['dia_chi']
        password = request.form['password']
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        connection = create_connection()
        
        res = execute_query(connection, procedure='AddKhachHang', params=(ho_va_ten, sdt, email, dia_chi, hashed_password))
        if res and res[0][0] == 'Email already registered':
            flash('Email đã tồn tại')
            return redirect(url_for('register.register'))
        return redirect(url_for('login.login'))
    return render_template('register.html')