from flask import Blueprint, render_template, request, redirect, session
from .. import db
from ..models import User, Product, CartItem

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db.session.add(User(username=username, password=password))
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/')
    return render_template('login.html')

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    user_id = session.get('user_id')
    if user_id:
        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            db.session.add(CartItem(user_id=user_id, product_id=product_id, quantity=1))
        db.session.commit()
    return redirect('/')
