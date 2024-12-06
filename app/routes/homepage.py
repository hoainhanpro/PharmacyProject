from flask import Flask, render_template, request, Blueprint
import math
from datetime import datetime
from services.database import create_connection
from dotenv import load_dotenv
PRODUCTS_PER_PAGE = 12

load_dotenv()
homepage_bp = Blueprint('homepage', __name__)
app = Flask(__name__)

@app.template_filter('format_price')
def format_price(value):
    if isinstance(value, int) or isinstance(value, float):
        return '{:,.0f}'.format(value)
    return value

@homepage_bp.route('/')
def homepage():
    connection = create_connection()

    group = request.args.get("group", "") 
    type_ = request.args.get("type", "")  
    category = request.args.get("category", "") 
    search = request.args.get("search", "").lower() 
    page = int(request.args.get("page", 1)) 

    query = "SELECT webName, prices, primaryImage, ageUse FROM thuoc"

    filters = []

    if group == "over18":
        filters.append("ageUse IN ('Trên 18 tuổi', 'Trên 12 tuổi', 'Trên 8 tuổi', 'Trên 4 tuổi')")
    elif group == "over12":
        filters.append("ageUse IN ('Trên 12 tuổi', 'Trên 8 tuổi', 'Trên 4 tuổi')")
    elif group == "over8":
        filters.append("ageUse IN ('Trên 8 tuổi', 'Trên 4 tuổi')")
    elif group == "over4":
        filters.append("ageUse = 'Trên 4 tuổi'")
    
    if search:
        filters.append(f"LOWER(webName) LIKE '%{search}%'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    cur = connection.cursor()
    cur.execute(query)  
    total_products = len(cur.fetchall()) 
    total_pages = math.ceil(total_products / PRODUCTS_PER_PAGE) 

    start = (page - 1) * PRODUCTS_PER_PAGE
    query += f" LIMIT {start}, {PRODUCTS_PER_PAGE}"

    cur.execute(query) 
    products = cur.fetchall()
    has_products = len(products) > 0
    cur.close()
    connection.close()  

    
    
    return render_template(
        "homepage.html", 
        products=products, 
        total_pages=total_pages, 
        page=page,
        group=group,
        type=type_,
        category=category,
        search=search, 
        has_products=has_products
    )