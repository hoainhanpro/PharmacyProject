from flask import Blueprint, render_template, request, redirect, url_for

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your registration logic here
        return redirect(url_for('login.login'))
    return render_template('register.html')