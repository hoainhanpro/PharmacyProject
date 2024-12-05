from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.database import create_connection, execute_query

employeemanager_bp = Blueprint('employeemanager', __name__)

@employeemanager_bp.route('/employeemanager', methods=['GET', 'POST'])
def employeemanager():
    connection = create_connection()
    cur = connection.cursor(dictionary=True)
    
    # Xử lý phân trang
    page = request.args.get('page', 1, type=int)
    limit = 10  # Số nhân viên trên mỗi trang
    offset = (page - 1) * limit
    
    # Lấy tổng số nhân viên
    cur.execute("SELECT COUNT(*) as total FROM nhanvien")
    total_employees = cur.fetchone()['total']
    total_pages = (total_employees + limit - 1) // limit  # Làm tròn lên
    
    # Lấy danh sách nhân viên theo trang
    cur.execute(f"SELECT * FROM nhanvien LIMIT {limit} OFFSET {offset}")
    employees = cur.fetchall()
    
    if request.method == 'POST':
        action = request.form.get('action')
        print(f"Action: {action}")  # Debug
        print(f"Form data: {request.form}")  # Debug
        
        if action == 'add':
            try:
                # Kiểm tra mã nhân viên đã tồn tại
                employee_id = request.form['id']
                cur.execute("SELECT * FROM nhanvien WHERE id = %s", (employee_id,))
                existing_employee = cur.fetchone()
                
                if existing_employee:
                    flash('Mã nhân viên đã tồn tại!', 'error')
                else:
                    cur.callproc('AddNhanVien', (
                        employee_id,
                        request.form['ho_va_ten'],
                        request.form['sdt'],
                        request.form['email'],
                        request.form['dia_chi'],
                        request.form['password'],
                        request.form['type_nhanvien']
                    ))
                    connection.commit()
                    print("Thêm nhân viên thành công")  # Debug
                    flash('Thêm nhân viên thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi thêm nhân viên: {str(e)}")  # Debug
                connection.rollback()
                flash(f'Lỗi khi thêm nhân viên: {str(e)}', 'error')
        
        elif action == 'delete':
            try:
                employee_id = request.form['id']
                print(f"Đang xóa nhân viên có ID: {employee_id}")  # Debug
                cur.callproc('DeleteNhanVien', (employee_id,))
                connection.commit()
                print("Xóa nhân viên thành công")  # Debug
                flash('Xóa nhân viên thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi xóa nhân viên: {str(e)}")  # Debug
                connection.rollback()
                flash(f'Lỗi khi xóa nhân viên: {str(e)}', 'error')
        
        elif action == 'update':
            try:
                cur.callproc('UpdateNhanVien', (
                    request.form['id'],
                    request.form['ho_va_ten'],
                    request.form['sdt'],
                    request.form['email'],
                    request.form['dia_chi'],
                    request.form['password'],
                    request.form['type_nhanvien']
                ))
                connection.commit()
                print("Cập nhật nhân viên thành công")  # Debug
                flash('Cập nhật nhân viên thành công!', 'success')
            except Exception as e:
                print(f"Lỗi khi cập nhật nhân viên: {str(e)}")  # Debug
                connection.rollback()
                flash(f'Lỗi khi cập nhật nhân viên: {str(e)}', 'error')
        
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('employeemanager.employeemanager'))
    
    return render_template('employeemanager.html', 
                         employees=employees,
                         current_page=page,
                         total_pages=total_pages)