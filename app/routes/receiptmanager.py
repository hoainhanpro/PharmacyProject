from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.database import create_connection, execute_query

receiptmanager_bp = Blueprint('receiptmanager', __name__)

@receiptmanager_bp.route('/danh_sach_hoa_don')
def danh_sach_hoa_don():
    connection = create_connection()
    
    query = '''
        SELECT hoadon.*, KhachHang.ho_va_ten
        FROM hoadon
        JOIN KhachHang ON hoadon.idkh = KhachHang.id
        WHERE hoadon.trangThai = 'da thanh toan'
    '''
    danh_sach_hoa_don = execute_query(connection, query)
    print(danh_sach_hoa_don)
    return render_template('receiptmanager.html', danh_sach_hoa_don=danh_sach_hoa_don)

@receiptmanager_bp.route('/chi_tiet_hoa_don/<int:idhd>/<int:idkh>')
def chi_tiet_hoa_don(idhd, idkh):
    connection = create_connection()

    query = f"""
        SELECT ct.idThuoc, t.webName, t.primaryImage, ct.soLuong, ct.giaTien
        FROM chitiethoadon ct
        JOIN thuoc t ON ct.idThuoc = t.id
        WHERE ct.idhd = {idhd} AND ct.idhd IN (SELECT id FROM hoadon WHERE idkh = {idkh})
    """
    order_details = execute_query(connection, query)

    return render_template('order_details.html', order_details=order_details, idkh=idkh)

