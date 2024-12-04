from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import os
import math
from datetime import datetime
from services.database import create_connection
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
paid_orders_bp = Blueprint('paid_orders', __name__)
app.secret_key = os.urandom(24)

@paid_orders_bp.route('/paid_orders')
def paid_orders():
    idkh = session['user'][0]
    if not idkh:
        return redirect(url_for('login')) 

    connection = create_connection()
    cur = connection.cursor()

    query = """
        SELECT id, tongTien, trangThai
        FROM hoadon
        WHERE idkh = %s AND trangThai = 'da thanh toan'
    """
    cur.execute(query, (idkh,))
    paid_orders = cur.fetchall()

    cur.close()
    connection.close()

    return render_template('paid_orders.html', paid_orders=paid_orders, idkh=idkh)

@paid_orders_bp.route('/order_details/<int:idhd>/<int:idkh>')
def order_details(idhd, idkh):
    connection = create_connection()
    cur = connection.cursor()
    query = """
        SELECT ct.idThuoc, t.webName, t.primaryImage, ct.soLuong, ct.giaTien
        FROM chitiethoadon ct
        JOIN thuoc t ON ct.idThuoc = t.id
        WHERE ct.idhd = %s AND ct.idhd IN (SELECT id FROM hoadon WHERE idkh = %s)
    """
    cur.execute(query, (idhd, idkh))
    order_details = cur.fetchall()

    cur.close()
    connection.close()

    return render_template('order_details.html', order_details=order_details, idkh=idkh)