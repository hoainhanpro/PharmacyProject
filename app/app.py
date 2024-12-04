from flask import Flask, redirect, url_for
from routes import login_bp, register_bp, homepage_bp, cart_bp, paid_orders_bp, medicinemanager_bp, product_detail_bp
import os
from dotenv import load_dotenv
from services import create_connection, execute_query

load_dotenv()

app = Flask(__name__)

app.secret_key=os.getenv('PASSWORD')

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(paid_orders_bp)
app.register_blueprint(medicinemanager_bp)
app.register_blueprint(product_detail_bp)

if __name__ == '__main__':
    app.run(debug=True)