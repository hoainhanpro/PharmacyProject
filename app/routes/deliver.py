import datetime
from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for, flash
from services.database import create_connection, execute_query

deliver_bp = Blueprint('deliver', __name__)

@deliver_bp.route('/deliverlisting')
def deliverlisting():
    connection = create_connection()
    query = '''
    SELECT hoadon.*, KhachHang.ho_va_ten, KhachHang.sdt, KhachHang.dia_chi
    FROM hoadon
    JOIN KhachHang ON hoadon.idkh = KhachHang.id
    LEFT JOIN dongiaohang ON hoadon.id = dongiaohang.idhd
    WHERE hoadon.trangThai = 'da thanh toan' AND dongiaohang.id IS NULL
    '''
    danh_sach_hoa_don = execute_query(connection, query)
    return render_template('deliverlisting.html', danh_sach_hoa_don=danh_sach_hoa_don)

@deliver_bp.route('/mydeliveries')
def mydeliveries():
    connection = create_connection()
    query = f'''
    SELECT hoadon.*, KhachHang.ho_va_ten, KhachHang.sdt, KhachHang.dia_chi, dongiaohang.ngay_giao
    FROM hoadon
    JOIN KhachHang ON hoadon.idkh = KhachHang.id
    JOIN dongiaohang ON hoadon.id = dongiaohang.idhd
    WHERE dongiaohang.idnv = {session.get('user')[0]}
    '''
    danh_sach_hoa_don = execute_query(connection, query)
    return render_template('mydeliveries.html', danh_sach_hoa_don=danh_sach_hoa_don)

@deliver_bp.route('/nhan_don/<int:idhd>', methods=['POST'])
def nhan_don(idhd):
    connection = create_connection()
    query = f'''
    INSERT INTO dongiaohang(idhd, idnv)
    VALUES ({idhd}, {session.get('user')[0]})
    '''
    execute_query(connection, query)
    return jsonify({'status': 'success'})

@deliver_bp.route('/hoan_thanh/<int:idhd>', methods=['POST'])
def hoan_thanh(idhd):
    ngay_giao = datetime.datetime.now().strftime('%Y-%m-%d')

    connection = create_connection()
    query = f'''
        UPDATE dongiaohang
        SET ngay_giao = '{ngay_giao}'
        WHERE idhd = {idhd}
    '''
    execute_query(connection, query)
    return jsonify({'success': True})
