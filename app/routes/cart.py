from flask import Flask, render_template, redirect, session, url_for, Blueprint, flash
from services.database import create_connection
from dotenv import load_dotenv

# load_dotenv()
# app = Flask(__name__)
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    connection = create_connection()
    cur = connection.cursor()
    idkh = session['user'][0]

    query = """
        SELECT ct.idThuoc, t.webName, t.primaryImage, ct.soLuong, ct.giaTien, ct.idhd
        FROM chitiethoadon ct
        JOIN thuoc t ON ct.idThuoc = t.id
        WHERE ct.idhd IN (SELECT id FROM hoadon WHERE idkh = %s AND trangThai = 'chua thanh toan')
    """
    cur.execute(query, (idkh,))
    cart_items = cur.fetchall()

    grouped_cart_items = {}

    for item in cart_items:
        product_id = item[0]
        if product_id in grouped_cart_items:
            grouped_cart_items[product_id]['soLuong'] += item[3]
        else:
            grouped_cart_items[product_id] = {
                'webName': item[1],
                'primaryImage': item[2],
                'soLuong': item[3],
                'giaTien': item[4],
                'idThuoc': product_id,
            }

    final_cart_items = list(grouped_cart_items.values())

    total_value = sum(item['soLuong'] * item['giaTien'] for item in final_cart_items)

    cur.close()
    connection.close()

    return render_template('cart.html', cart_items=final_cart_items, total_value=total_value)

@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    connection = create_connection()
    cur = connection.cursor()

    idkh = session['user'][0]
    select_query = """
        SELECT id, soLuong
        FROM chitiethoadon
        WHERE idThuoc = %s AND idhd IN (SELECT id FROM hoadon WHERE idkh = %s)
        ORDER BY id DESC
    """
    cur.execute(select_query, (product_id, idkh))
    rows = cur.fetchall()

    if rows:
        closest_row_id = rows[0][0]
        closest_quantity = rows[0][1]

        if closest_quantity > 1:
            update_query = """
                UPDATE chitiethoadon
                SET soLuong = soLuong - 1
                WHERE id = %s
            """
            cur.execute(update_query, (closest_row_id,))
        else:
            delete_query = """
                DELETE FROM chitiethoadon
                WHERE id = %s
            """
            cur.execute(delete_query, (closest_row_id,))

    connection.commit()

    cur.close()
    connection.close()

    return redirect(url_for('cart.cart'))

@cart_bp.route('/process_payment', methods=['POST'])
def process_payment():
    connection = create_connection()
    cur = connection.cursor()
    idkh = session['user'][0]

    select_total_query = """
        SELECT SUM(ct.soLuong * ct.giaTien)
        FROM chitiethoadon ct
        JOIN hoadon h ON ct.idhd = h.id
        WHERE h.idkh = %s AND h.trangThai = 'chua thanh toan'
    """
    cur.execute(select_total_query, (idkh,))
    total_value = cur.fetchone()[0] 

    select_cart_items_query = """
        SELECT ct.idThuoc, t.webName, ct.soLuong
        FROM chitiethoadon ct
        JOIN thuoc t ON ct.idThuoc = t.id
        JOIN hoadon h ON ct.idhd = h.id
        WHERE h.idkh = %s AND h.trangThai = 'chua thanh toan'
    """
    cur.execute(select_cart_items_query, (idkh,))
    cart_items = cur.fetchall()

    insufficient_items = []

    for id_thuoc, web_name, so_luong in cart_items:
        update_quantity_query = """
            UPDATE thuoc
            SET quantity = quantity - %s
            WHERE id = %s AND quantity >= %s
        """
        cur.execute(update_quantity_query, (so_luong, id_thuoc, so_luong))

        if cur.rowcount == 0:  
            insufficient_items.append(web_name)

    if insufficient_items:
        connection.rollback()
        cur.close()
        connection.close()
        flash("Không đủ hàng trong kho cho các sản phẩm: " + ", ".join(insufficient_items), 'danger')
        return redirect(url_for('cart.cart'))

    update_status_query = """
        UPDATE hoadon
        SET tongTien = %s, trangThai = 'da thanh toan'
        WHERE idkh = %s AND trangThai = 'chua thanh toan'
    """
    cur.execute(update_status_query, (total_value, idkh))

    connection.commit()
    cur.close()
    connection.close()

    flash("Thanh toán thành công!", 'success')
    return redirect(url_for('cart.cart'))

@cart_bp.route('/cancel_order', methods=['POST'])
def cancel_order():
    connection = create_connection()
    cur = connection.cursor()

    idkh = session['user'][0]
    update_status_query = """
        UPDATE hoadon
        SET trangThai = 'da huy'
        WHERE idkh = %s AND trangThai = 'chua thanh toan'
    """
    cur.execute(update_status_query, (idkh,))

    delete_query = """
        DELETE FROM chitiethoadon
        WHERE idhd IN (SELECT id FROM hoadon WHERE idkh = %s AND trangThai = 'da huy')
    """
    cur.execute(delete_query, (idkh,))

    connection.commit()
    cur.close()
    connection.close()

    return redirect(url_for('cart.cart'))
