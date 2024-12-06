from flask import Flask, render_template, request, Blueprint, session, redirect, url_for, flash
import math
from datetime import datetime
from services.database import create_connection
from dotenv import load_dotenv

load_dotenv()
userinfo_bp = Blueprint('userinfo', __name__)
app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@userinfo_bp.route('/userinfo', methods=['GET', 'POST'])
def user_info():
    user_id = session['user'][0] 
    connection = create_connection()

    if request.method == 'GET':
        query = "SELECT ho_va_ten, sdt, email, dia_chi FROM khachhang WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

    if request.method == 'POST':
        ho_va_ten = request.form['ho_va_ten']
        sdt = request.form['sdt']
        email = request.form['email']
        dia_chi = request.form['dia_chi']

        query = """
            UPDATE khachhang 
            SET ho_va_ten = %s, sdt = %s, email = %s, dia_chi = %s 
            WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (ho_va_ten, sdt, email, dia_chi, user_id))
            connection.commit()

        flash('Cập nhật thông tin thành công!', 'success')

        return redirect(url_for('userinfo.user_info'))

    connection.close()
    
    return render_template('userinfo.html', user=user)
