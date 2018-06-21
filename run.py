from flask import Flask, request, send_from_directory, jsonify

app = Flask('amazon')


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'product.html')



products=[]


@app.route('/api/products', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        search_query = request.args['name']
        for prod in products:
            if prod['name'] == search_query:
                return jsonify(prod)
        return "no_match"
    elif request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        prod = {
             'name': name,
             'desc': desc,
             'price': price
         }
        products.append(prod)
        return send_from_directory('static', 'product.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)