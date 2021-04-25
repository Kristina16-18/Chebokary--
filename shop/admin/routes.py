from flask import render_template
from shop import app
from shop.products.models import AddBook,Genre


# чтобы войти в режим админа, нужно написать /admin
@app.route('/admin')
def admin():
    products = AddBook.query.all()
    return render_template('admin/index.html', title='Страница админа',products=products)

@app.route('/genres')
def genres():
    genres = Genre.query.order_by(Genre.id.desc()).all()
    return render_template('admin/genre.html', title='genres',genres=genres)