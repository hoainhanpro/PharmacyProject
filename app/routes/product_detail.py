from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, flash
import os
import math
from datetime import datetime
from services.database import create_connection
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)
product_detail_bp = Blueprint('product_detail', __name__)


@product_detail_bp.route('/product/<webName>')
def product_detail(webName):
    connection = create_connection()
    cur = connection.cursor()
    
    query = "SELECT * FROM thuoc WHERE webName = %s"
    cur.execute(query, (webName,))
    product = cur.fetchone()

    cur.close()
    connection.close()

    if product:
        try:
            price = float(product[15])  
            formatted_price = "{:,.0f}".format(price)  
        except ValueError:
            formatted_price = product[15]

        return render_template("product_detail.html", product=product, formatted_price=formatted_price)
    else:
        return "Sản phẩm không tồn tại", 404

@product_detail_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        quantity = int(request.form.get('quantity', 1)) 
        webName = request.form.get('webName') 
        
        connection = create_connection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM thuoc WHERE webName = %s", (webName,))
        product = cur.fetchone()
        
        if not product:
            return redirect(url_for('homepage'))
        
        idkh = session['user'][0]
        product_id = product[0]
        price = float(product[15])
        cur.execute("SELECT id FROM hoadon WHERE idkh = %s AND trangThai = 'chua thanh toan'", (idkh,))
        existing_invoice = cur.fetchone()

        if existing_invoice:
            idhd = existing_invoice[0]
        else:
            cur.execute("""
                INSERT INTO hoadon (idkh, tongTien, trangThai)
                VALUES (%s, %s, %s)
            """, (idkh, 0.0, 'chua thanh toan'))
            connection.commit()
            idhd = cur.lastrowid  

        cur.execute("""
            INSERT INTO chitiethoadon (idhd, idThuoc, soLuong, giaTien, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (idhd, product_id, quantity, price, datetime.utcnow()))
        connection.commit()

        cur.execute("""
            UPDATE hoadon
            SET tongTien = (SELECT SUM(soLuong * giaTien) FROM chitiethoadon WHERE idhd = %s)
            WHERE id = %s
        """, (idhd, idhd))
        connection.commit()

        cur.close()
        connection.close()
        flash("Đã thêm sản phẩm vào giỏ hàng thành công!", "success")
        return redirect(url_for('product_detail.product_detail', webName=webName))

    except Exception as e:
        flash("Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng.", "danger")
        return redirect(url_for('product_detail.product_detail', webName=webName))



