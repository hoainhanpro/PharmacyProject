from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.database import create_connection, execute_query
import hashlib

medicinemanager_bp = Blueprint('medicinemanager', __name__)

@medicinemanager_bp.route('/medicinemanager', methods=['GET', 'POST'])
def medicinemanager():
    connection = create_connection()
    cur = connection.cursor(dictionary=True)
    
    # Xử lý phân trang
    page = request.args.get('page', 1, type=int)
    limit = 12  # Số thuốc trên mỗi trang
    offset = (page - 1) * limit
    
    # Lấy tổng số thuốc
    cur.execute("SELECT COUNT(*) as total FROM thuoc")
    total_medicines = cur.fetchone()['total']
    total_pages = (total_medicines + limit - 1) // limit  # Làm tròn lên
    
    # Lấy danh sách thuốc theo trang
    cur.execute(f"SELECT * FROM thuoc LIMIT {limit} OFFSET {offset}")
    medicines = cur.fetchall()
    
    if request.method == 'POST':
        action = request.form.get('action')
        print(f"Action: {action}")  # Debug
        print(f"Form data: {request.form}")  # Debug
        
        if action == 'add':
            try:
                # Thêm thuốc vào database
                cur.callproc('AddThuoc', (
                    request.form['id'],
                    request.form['headingText'],
                    request.form['dosage'],
                    request.form['ageUse'],
                    request.form['shortName'],
                    request.form['shortDescription'],
                    request.form['preservation'],
                    request.form['adverseEffect'],
                    request.form['producer'],
                    request.form['tusage'],
                    request.form['tname'],
                    request.form['ingredient'],
                    request.form['primaryImage'],
                    request.form['careful'],
                    request.form['webName'],
                    request.form['prices'],
                    request.form['specification'],
                    request.form['warning'],
                    request.form['brand'],
                    request.form['brandOrigin'],
                    request.form['quantity']
                ))
                connection.commit()
                print("Thêm thuốc thành công")  # Debug
                flash('Thêm thuốc thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi thêm thuốc: {str(e)}")  # Debug
                connection.rollback()
                flash(f'Lỗi khi thêm thuốc: {str(e)}', 'error')
        
        elif action == 'delete':
            try:
                # Xóa thuốc trong database
                medicine_id = request.form['id']
                print(f"Đang xóa thuốc có ID: {medicine_id}")  # Debug
                cur.callproc('DeleteThuoc', (medicine_id,))
                connection.commit()
                print("Xóa thuốc thành công")  # Debug
                flash('Xóa thuốc thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi xóa thuốc: {str(e)}")  # Debug
                connection.rollback()
                flash(f'Lỗi khi xóa thuốc: {str(e)}', 'error')
        
        elif action == 'update':
            try:
                # Cập nhật thuốc trong database
                cur.callproc('UpdateThuoc', (
                    request.form['id'],
                    request.form['headingText'],
                    request.form['dosage'],
                    request.form['ageUse'],
                    request.form['shortName'],
                    request.form['shortDescription'],
                    request.form['preservation'],
                    request.form['adverseEffect'],
                    request.form['producer'],
                    request.form['tusage'],
                    request.form['tname'],
                    request.form['ingredient'],
                    request.form['primaryImage'],
                    request.form['careful'],
                    request.form['webName'],
                    request.form['prices'],
                    request.form['specification'],
                    request.form['warning'],
                    request.form['brand'],
                    request.form['brandOrigin'],
                    request.form['quantity']
                ))
                connection.commit()
                print("Cập nhật thuốc thành công")  # Debug
                flash('Cập nhật thuốc thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi cập nhật thuốc: {str(e)}")  # Debug
                connection.rollback()
                flash(f'Lỗi khi cập nhật thuốc: {str(e)}', 'error')
        
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('medicinemanager.medicinemanager'))
    
    return render_template('medicinemanager.html', 
                         medicines=medicines, 
                         current_page=page,
                         total_pages=total_pages)

    
    

