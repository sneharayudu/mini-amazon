from flask import send_from_directory,request,render_template,session
from amazon import app
from amazon.model import product as product_model
from amazon.model import user as user_model
from bson.objectid import ObjectId


@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        user_details = user_model.search_by_user_id(session['user_id'])
        return render_template('home.html',name = user_details['name'])
    else:
        return render_template('index.html', message='20% off with paypal')


@app.route('/admin', methods=['GET'])
def admin():
    if 'user_id' in session:
        user_details = user_model.search_by_user_id(session['user_id'])
        return render_template('admin.html',name = user_details['name'])
    else:
        return render_template('index.html', message='20% off with paypal')


@app.route('/api/logout',methods=['GET'])
def remove():
    session.clear()
    return render_template('index.html',message = 'succesfully logged out')


@app.route('/api/product',methods=['POST','GET'])
def product():
    if request.method == 'GET':
        query_name=request.args['name']
        matching_products = product_model.search_by_name(query_name)
        return render_template('admin_results.html',query=query_name,results=matching_products)

    elif request.method == 'POST':
        op_type = request.form['op_type']
        if op_type == 'add':
            prod = {
                'name': request.form['name'],
                'desc': request.form['desc'],
                'price': int(request.form['price'])
            }
            sucesss = product_model.add_product(prod)
            if sucesss:
                return render_template('admin.html',message = 'added product')
            else:
                return render_template('admin.html',message = 'not able to add product')

        elif op_type == 'update':
            p_id = request.form['product_id']
            updates = {}
            if request.form['name'] != '':
                updates['name'] = request.form['name']
            if request.form['desc'] != '':
                updates['desc'] = request.form['desc']
            if request.form['price'] != '':
                updates['price'] = request.form['price']
            updated_product = {
                '$set' : updates
            }
            prod_id = {'_id' : ObjectId(p_id)}
            update = product_model.update_product(prod_id,updated_product)
            if update:
                return render_template('admin.html',message = 'updated product')
            else:
                return render_template('admin.html',message = 'unable to update product')
        if op_type == 'delete':
            p_id = request.form['product_id']
            prod_id = {'_id':ObjectId(p_id)}
            sucesss = product_model.delete_product(prod_id)
            if sucesss:
                return render_template('admin.html',message = 'deleted product')
            else:
                return render_template('admin.html',message = 'not able to delete product')


@app.route('/api/user',methods=['GET','POST'])
def user():
    if request.method == 'GET':
        query_name=request.args['name']
        matching_products = product_model.search_by_name(query_name)

        #return first matching output

        return render_template('results.html',query=query_name,results=matching_products)

    # to login and signup
    op_type = request.form['op_type']

    if op_type == 'login':
        username = request.form['username']
        password = request.form['password']
        success = user_model.authenticate(username, password)
        if success:
            user_details = user_model.search_by_username(username)
            session['user_id'] = str(user_details['_id'])
            if username == 'admin':
                return  render_template('admin.html',message = 'welcome admin')
            else:
                return render_template('home.html', message = 'sucessfull login')
        else:
            return render_template('index.html', message='unsucessfull login')

    elif op_type == 'signup':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        success = user_model.signup_user(name, username, password)
        if success:
            user_details = user_model.search_by_username(username)
            session['user_id']=str(user_details['_id'])
            return render_template('home.html', message = 'signed up')
        else:
            return render_template('index.html', message = 'username exists' )
    else:
        # take user back to admin page
        return render_template('index.html', message = 'some_wrong')


@app.route('/api/cart', methods = ['POST'])
def cart():
    op_type = request.form['op_type']
    user_id = session['user_id']
    user_details = user_model.search_by_user_id(user_id)
    if op_type == 'add_cart':
        product_id = request.form['product_id']
        user_model.add_to_cart(user_id, product_id)
        return render_template('home.html',name=user_details['name'])

    elif op_type == 'delete':
        product_id = request.form['product_id']
        sucess = user_model.delete_from_cart(user_id, product_id)
        if sucess:
            cart_items_ids = user_model.retrive_cart(user_id)
            cart_items = []
            for p_id in cart_items_ids:
                cart_items.append(product_model.get_details(p_id))
            return render_template('cart.html', results=cart_items, name=user_details['name'])
        else:
            return render_template('results.html',message = "unable to delete product from cart")
    elif op_type == 'retrive':
        cart_items_ids = user_model.retrive_cart(user_id)
        cart_items = []
        total =0
        for p_id in cart_items_ids:
            cart_item =product_model.get_details(p_id)
            cart_items.append(cart_item)
            total += int(cart_item['price'])
        return render_template('cart.html',results=cart_items,name = user_details['name'],total = total)






