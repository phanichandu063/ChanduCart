from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Example products (mobiles)
products = [
    {'id': 1, 'name': 'iPhone 15 Pro Max', 'price': 149999, 'image': 'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/iphone-15-pro-max'},
    {'id': 2, 'name': 'Samsung Galaxy S24 Ultra', 'price': 129999, 'image': 'https://images.samsung.com/is/image/samsung/assets/in/smartphones/galaxy-s24-ultra'},
    {'id': 3, 'name': 'Realme GT 6 Pro', 'price': 45999, 'image': 'https://image01.realme.net/general/20240621/gt6.png'},
    {'id': 4, 'name': 'iQOO Neo 9 Pro', 'price': 36999, 'image': 'https://www.iqoo.com/media/neo9pro.png'},
]

cart = []

@app.route('/')
def home():
    return render_template('home.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    for product in products:
        if product['id'] == product_id:
            # Check if already in cart
            for item in cart:
                if item['id'] == product_id:
                    item['quantity'] += 1
                    break
            else:
                cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'image': product['image'], 'quantity': 1})
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    action = request.form.get('action')
    for item in cart:
        if item['id'] == product_id:
            if action == 'increase':
                item['quantity'] += 1
            elif action == 'decrease':
                item['quantity'] -= 1
                if item['quantity'] <= 0:
                    cart.remove(item)
            elif action == 'remove':
                cart.remove(item)
            break
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)