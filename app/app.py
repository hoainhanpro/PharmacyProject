from flask import Flask, abort, redirect, render_template, request, session, url_for
from routes import login_bp, register_bp, homepage_bp, cart_bp, paid_orders_bp, medicinemanager_bp, product_detail_bp, receiptmanager_bp, datasetmanager_bp, employeemanager_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('PASSWORD')

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(paid_orders_bp)
app.register_blueprint(medicinemanager_bp)
app.register_blueprint(product_detail_bp)
app.register_blueprint(receiptmanager_bp)
app.register_blueprint(datasetmanager_bp)
app.register_blueprint(employeemanager_bp)

# @app.before_request
# def check_permissions():
#     roles_permissions = {
#         'nhanvien': {'receiptmanager.danh_sach_hoa_don', 'receiptmanager.chi_tiet_hoa_don',
#                      'medicinemanager.medicinemanager', 'datasetmanager.dataset'},
#         'khachhang': {'cart.cart', 'cart.remove_from_cart',
#                       'paid_orders.paid_orders', 'cart.cancel_order', 'product_detail.add_to_cart'},
#     }
#     endpoint = request.endpoint

#     if endpoint in ['login.login', 'login.logout', 'register.register', 'homepage.homepage', 'static', 'product_detail.product_detail']:
#         return

#     if 'user' not in session:
#         return redirect(url_for('login.login'))

#     user_role = session.get('role')

#     allowed_endpoints = roles_permissions.get(user_role, set())
#     if endpoint not in allowed_endpoints:
#         abort(403)


# @app.errorhandler(403)
# def forbidden(error):
#     return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(debug=True)
