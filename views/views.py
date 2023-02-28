from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

# website routes
@views_bp.route('/buy')
@views_bp.route('/pricing')
def buy():
    return render_template('buy.html')

@views_bp.route('/')
@views_bp.route('/playground')
def playground():
    return render_template('playground.html')

@views_bp.route('/signup')
def signup():
    return render_template('signup.html')

@views_bp.route('/login')
def login():
    return render_template('login.html')

@views_bp.route('/home')
def home():
    return render_template('home.html')