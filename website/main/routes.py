from main import app
# from main import db
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from main.forms import LoginForm

@app.errorhandler(404)
def page_not_found(e):
    return redirect('home')

@app.errorhandler(500)
def page_not_found(e):
    return redirect('home')

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # return render_template('login.html', title='login')
    return render_template(
        'base_simple.html',
        title='home'
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = ''
        if User.query.filter_by(email=form.email.data).first():
            user = User.query.filter_by(email=form.email.data).first()

        # user = User.query.filter_by(displayname=form.displayname.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
        else:
            flash('Login Unsuccessful. Check displayname/email and Password')

    return render_template(
        'user/login.html',
        title='Login',
        form=form
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(request.referrer)

