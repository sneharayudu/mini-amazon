from amazon.model import db
import pymongo
from bson.objectid import ObjectId


def search_by_name(name):
    query = {'name':name}
    matching_products = db['products'].find(query)
    matching_products.sort([('price', pymongo.DESCENDING)])
    return list(matching_products)


def add_product(product):
    db['products'].insert_one(product)
    return True


def update_product(p_id, updated_product):
    filters = p_id
    sucess = db['products'].update_one(filter=filters,update = updated_product)
    if sucess:
        return True
    else:
        return False


def get_details(p_id):
    condition = {'_id': ObjectId(p_id)}
    cursor = db['products'].find(condition)
    if cursor.count() == 1:
        user_data = cursor[0]
        return user_data
    else:
        return None


def delete_product(product_id):
    sucess = db['products'].delete_one(product_id)
    if sucess:
        return True
    else:
        return False