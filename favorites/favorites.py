from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import db, app
from shop.products.models import AddBook
from shop.products.routes import genres


def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addfav', methods=['POST'])
def AddFav():
    try:
        product_id = request.form.get('product_id')
        product = AddBook.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'author':product.author,'image':product.image}}
            if 'FavoriteBooks' in session:
                print(session['FavoriteBooks'])
                if product_id in session['FavoriteBooks']:
                    for key, item in session['FavoriteBooks'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                else:
                    session['FavoriteBooks'] = MagerDicts(session['FavoriteBooks'], DictItems)
                    return redirect(request.referrer)
            else:
                session['FavoriteBooks'] = DictItems
                return redirect(request.referrer)       
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/favourite')
def getFav():
    if 'FavoriteBooks' not in session or len(session['FavoriteBooks']) <= 0:
        return redirect(url_for('home'))
    return render_template('products/favorites.html',genres=genres())


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'FavoriteBooks' not in session or len(session['FavoriteBooks']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['FavoriteBooks'].items():
            if int(key) == id:
                session['FavoriteBooks'].pop(key, None)
                return redirect(url_for('getFav'))
    except Exception as e:
        print(e)
        return redirect(url_for('getFav'))


@app.route('/clearfav')
def clearfav():
    try:
        session.pop('FavoriteBooks', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
