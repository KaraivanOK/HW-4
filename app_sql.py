from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)
app.app_context().push()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    alcohol = db.Column(db.String(10))
    specification = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Product %r>' % self.id


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/products', methods=['GET'])
def get_query_product():
    query_products = []
    name = request.args.get('name')
    products = Product.query.all()
    if name:
        for product in products:
            if product.name.lower() == name.lower() or name.lower() in product.name.lower():
                query_products.append(product)
        return render_template('query_products.html', query_products=query_products)
    else:
        return render_template('products.html', products=products)


@app.route('/products/<int:id>')
def get_product(id):
    product = Product.query.get(id)
    return render_template('product.html', product=product)


@app.route('/products/<int:id>/del')
def product_delete(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/products')
    except:
        return 'An error occurred while deleting the product.'


@app.route('/products/<int:id>/update', methods=['POST', 'GET'])
def product_update(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.specification = request.form['specification']
        product.alcohol = request.form['alcohol']

        try:
            db.session.commit()
            return redirect('/products')
        except:
            return 'An error occurred while modifying the product.'
    else:
        return render_template('product_update.html', product=product)


@app.route('/create_product', methods=['POST', 'GET'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        specification = request.form['specification']
        alcohol = request.form['alcohol']

        product = Product(name=name, price=price, alcohol=alcohol, specification=specification)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/products')
        except:
            return 'There was an error adding the product'
    else:
        return render_template('create_product.html')


if __name__ == '__main__':
    app.run(debug=True)
