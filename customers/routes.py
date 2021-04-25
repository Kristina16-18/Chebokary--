from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_user
from shop import app, db, bcrypt
from .forms import CustomerRegisterForm, CustomerLoginFrom
from .model import Register


@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(register)
        flash(f'Добро пожаловать, {form.name.data}! Спасибо за регистрацию!', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = db.session.query(Register).filter(Register.email==form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Неправильный логин или пароль','danger')
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))
