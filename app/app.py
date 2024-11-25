from flask import Flask, redirect, url_for
from routes import login_bp, register_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key=os.getenv('PASSWORD')

@app.route('/')
def home():
    return redirect(url_for('login.login'))

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)

if __name__ == '__main__':
    app.run(debug=True)