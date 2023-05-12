from flask import Blueprint, render_template, session, redirect

from models.user import User

views_bp = Blueprint('views', __name__)


# website routes
@views_bp.route('/buy')
def buy():
    return render_template('buy.html')


@views_bp.route('/pricing')
def pricing():
    return render_template('pricing.html')


@views_bp.route('/playground')
def playground():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/signup")
    user = User.get_by_id(user_id)
    print(user.id, user.email, "user_id ")
    if user.billing_status == "active":
        return render_template('playground.html')
    else:
        return redirect('/pricing')


@views_bp.route('/batch_upload')
def batch_upload():
    table_data = 0
    return render_template('batch_upload.html', table_data=table_data)


@views_bp.route('/signup')
def signup():
    return render_template('signup.html')


@views_bp.route('/login')
def login():
    return render_template('login.html')


@views_bp.route('/reset')
def reset():
    return render_template('reset.html')


@views_bp.route('/')
@views_bp.route('/home')
def home():
    return render_template('home.html')


@views_bp.route('/api')
def api():
    return render_template('api.html')
