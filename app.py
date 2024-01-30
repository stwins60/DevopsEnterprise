from flask import Flask, jsonify, request
from flask_cors import CORS
import requests as r
import json

app = Flask(__name__)
CORS(app)

def get_products():
    products = r.get('https://dummyjson.com/products')
    return products.json()['products']


@app.route('/products', methods=['GET'])
def products():
    return jsonify(get_products())



@app.route('/products/<int:id>', methods=['GET'])
def product(id):
    products = get_products()
    for product in products:
        if product['id'] == id:
            return jsonify(product)
    return jsonify({'message': 'Product not found'})


@app.route('/products', methods=['POST'])
def add_product():
    products = get_products()
    new_product = request.get_json()
    products.append(new_product)
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)