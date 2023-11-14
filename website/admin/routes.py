from flask import render_template,session, request,redirect,url_for,flash
from website import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from website.products.models import Addproduct,Category,Brand
from website.customers.model import Register
from flask_login import login_required, current_user, logout_user, login_user

@app.route('/admin')
def admin():
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page',products=products)


@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands',brands=brands)


@app.route('/categories')
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)

@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'welcome {form.name.data} Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/admin/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} you are logged in now','success')
            return redirect(url_for('admin'))
        else:
            flash(f'Wrong email and password', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)

@app.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/delete-user/<int:user_id>', methods=['GET','POST'])
def delete_user(user_id):
    user_to_delete = Register.query.get(user_id)

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()

    return redirect(url_for('manage_accounts'))

@app.route('/admin/manage-user-accounts',methods=['GET','POST'])
def manage_accounts():
    user_list = Register.query.all()
    
    return render_template('admin/manage_users.html',user_data=user_list)