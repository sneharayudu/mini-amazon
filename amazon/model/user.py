from amazon.model import db
from bson.objectid import ObjectId


def search_by_user_id(user_id):
    # lets search for the user here
    query = {'_id': ObjectId(user_id)}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None


def search_by_username(username):
    # lets search for the user here
    query = {'username': username}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None


def signup_user(name, username, password):
    existing_user = search_by_username(username)
    if existing_user is not None:
        return False
    else:
        user = {
         'name': name,
         'username': username,
         'password': password,
         'cart': []
    }
    db['users'].insert_one(user)
    return True


def authenticate(username, password):
    user = search_by_username(username)

    if user is None:
        # user does not exist
        return False

    if user['password'] == password:
        # user exists and correct password
        return True
    else:
        # user exists but wrong password
        return False


def add_to_cart(user_id, product_id):
    condition = {'_id' : ObjectId(user_id)}
    cursor = db['users'].find(condition)

    if cursor.count() > 0:
        user_data = cursor[0]
    else:
        return False

    if 'cart' not in user_data:
        user_data['cart'] = []

    if product_id not in user_data['cart']:
        user_data['cart'].append(product_id)
        db['users'].update_one(filter=condition,update={'$set' : user_data})

    return True


def delete_from_cart(user_id,product_id):
    condition = {'_id': ObjectId(user_id)}
    cursor = db['users'].find(condition)
    if cursor.count() > 0:
        user_data = cursor[0]
        print (user_data)
    else:
        return False
    print(user_data['cart'])

    if product_id not in user_data['cart']:
        return False

    user_data['cart'].remove(product_id)
    cursor = db['users'].update_one(filter=condition, update={'$set': user_data})
    if cursor:
        return True
    else:
        return False


def retrive_cart(user_id):
    condition = {'_id': ObjectId(user_id)}
    cursor = db['users'].find(condition)
    cart_items=[]
    if cursor.count() == 1 :
        user_data = cursor[0]
        for p_id in  user_data['cart']:
            cart_items.append(p_id)
        return cart_items
    else:
        return False

