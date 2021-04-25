from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import app, db, search, photos
from .models import Genre, AddBook
from .forms import Book_obj
import secrets
import os


#здесь поиск и создание с редактированием и удалением жанров и книг
def genres():
    genres = Genre.query.join(AddBook, (Genre.id == AddBook.genre_id)).all()
    return genres


@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = AddBook.query.order_by(AddBook.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products, genres=genres())


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = AddBook.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products,genres=genres())


@app.route('/product/<int:id>')
def single_page(id):
    product = AddBook.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,genres=genres())


@app.route('/genre/<int:id>')
def get_genre(id):
    page = request.args.get('page',1, type=int)
    get_genre = Genre.query.filter_by(id=id).first_or_404()
    genre = AddBook.query.filter_by(genre=get_genre).paginate(page=page, per_page=8)
    return render_template('products/index.html',genre=genre,genres=genres(),get_genre=get_genre)


@app.route('/addgenre',methods=['GET','POST'])
def addgenre():
    if request.method =="POST":
        getgenre = request.form.get('genre')
        genre = Genre(name=getgenre)
        db.session.add(genre)
        flash(f'Жанр {getgenre} был добавлен','success')
        db.session.commit()
        return redirect(url_for('addgenre'))
    return render_template('products/addgenre.html', title='Add genre',genres='genres')


@app.route('/updategenre/<int:id>',methods=['GET','POST'])
def updategenre(id):
    if 'email' not in session:
        flash('Сначала выполните вход','danger')
        return redirect(url_for('login'))
    updategenre = Genre.query.get_or_404(id)
    genre = request.form.get('genre')
    if request.method =="POST":
        updategenre.name = genre
        flash(f'Жанр {updategenre.name} стал {genre}','success')
        db.session.commit()
        return redirect(url_for('genres'))
    genre = updategenre.name
    return render_template('products/addgenre.html', title='Изменить жанр',genres='genres',updategenre=updategenre)


@app.route('/deletegenre/<int:id>', methods=['GET','POST'])
def deletegenre(id):
    genre = Genre.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(genre)
        flash(f"Жанр {genre.name} был удалён","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"Жанр {genre.name} не может быть удалён", "warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = Book_obj(request.form)
    genres = Genre.query.all()
    if request.method == "POST" and 'image' in request.files:
        name = form.name.data
        author = form.author.data
        desc = form.discription.data
        genre = request.form.get('genre')
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        book = AddBook(name=name, author=author, desc=desc, genre_id=genre, image=image)
        db.session.add(book)
        flash(f'Книга {name} добавлена','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Добавить книгу', genres=genres)


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Book_obj(request.form)
    product = AddBook.query.get_or_404(id)
    genres = Genre.query.all()
    genre = request.form.get('genre')
    if request.method =="POST":
        product.name = form.name.data 
        product.author = form.author.data
        product.desc = form.discription.data
        product.genre_id = genre
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image))
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
            except:
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")

        flash('Информация о книге была обновлена','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.author.data = product.author
    form.discription.data = product.desc
    return render_template('products/addproduct.html', form=form, title='Редактирование книги',getproduct=product, genres=genres)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = AddBook.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'Книга "{product.name}" была удалена','success')
        return redirect(url_for('admin'))
    flash(f'Книга не удалена','success')
    return redirect(url_for('admin'))