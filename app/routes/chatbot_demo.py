from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from services.database import create_connection, execute_query

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/demo', methods=['GET', 'POST'])
def register():
    if 'chatMessages' in session:
        print(session['chatMessages'])
    return render_template('demo.html')