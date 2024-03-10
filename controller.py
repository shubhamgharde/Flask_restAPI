from config import *
from flask import request, jsonify
from model import Product
import json
#uri--> http://localhost:5000/api/v1/product/  --GET
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, get_jwt_identity, jwt_required
#from flask import Flask

from datetime import datetime
from datetime import timedelta
from datetime import timezone

app.config['JWT_SECRET_KEY'] = '1287A2^#&Dsb(@sdvhrtefwet'  #token configure hone ke liye sabse pehele kya hona chahiye
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=15)
jwt = JWTManager(app)


@app.route('/gettoken', methods=['POST'])
def validate_user():
    req_body = request.get_json()

    if req_body.get('USERNAME') == 'admin' and req_body.get('PASSWORD') == 'root123':
        atoken = create_access_token(identity=(req_body.get('USERNAME'), req_body.get('PASSWORD')))
        rtoken = create_refresh_token(identity=(req_body.get('USERNAME'), req_body.get('PASSWORD')))
        return json.dumps({"access_token": atoken, "refresh_token": rtoken})    #yahase jaisehi token mil jayega to kya return kar dunga mai
    else:
        return jsonify('Invalid credentials...!'), 401


@app.route('/api/v1/product/', methods=['GET'])   #http://localhost:5000/api/v1/product/
@jwt_required()
def get_list_of_products():
    #  Fetch list of product from db -- through sqlalchemy
    product_list = Product.query.all()

    #if no products in db -- return -- simple messege
    if not product_list:
        return json.dumps({"ERROR": "No Products...!"})
    final_product_list = []

    #iterate one by one and prepare dict--
    for prod in product_list:
        prod_dict = {}
        prod_dict['PRODUCT_ID'] = prod.id
        prod_dict['PRODUCT_NAME'] = prod.name
        prod_dict['PRODUCT_PRICE'] = prod.price
        prod_dict['PRODUCT_QYT'] = prod.qyt
        prod_dict['PRODUCT_VENDOR'] = prod.vendor
        prod_dict['PRODUCT_CATEGORY'] = prod.category

        # add that dict every time inside final list
        with app.app_context():
            final_product_list.append(prod_dict)

    if final_product_list:
        return json.dumps(final_product_list)

#uri--> http://localhost:5000/api/v1/product/  --POST


@app.route('/api/v1/product/', methods=['POST'])
@jwt_required()
def save_product():
    #print(request.__dict__)
    #print(dir(request))
    #print(request.get_json())
    req_data = request.get_json()  #req_data---is a dict
    if not req_data:
        return json.dumps({"ERROR": "Invalid Params to Create a Product"})

    MANDATORY_FIELD = ["PRODUCT_NAME", "PRODUCT_QYT", "PRODUCT_PRICE", "PRODUCT_CATEGORY", "PRODUCT_VENDOR"]

    keys = req_data.keys()
    print(keys)
    for mfield in MANDATORY_FIELD:
        if mfield not in keys:
            return json.dumps({"ERROR": f"{mfield} field id missing"})

    if str(req_data.get('PRODUCT_PRICE')).isalpha() or req_data.get('PRODUCT_PRICE') <= 0:
        return json.dumps({"ERROR": "Invalid Product Price"})

    try:
        prod = Product(name=req_data.get('PRODUCT_NAME'),
                       qyt=req_data.get('PRODUCT_QYT'),
                       price=req_data.get('PRODUCT_PRICE'),
                       category=req_data.get('PRODUCT_CATEGORY'),
                       vendor=req_data.get('PRODUCT_VENDOR'))

        with app.app_context():
            db.session.add(prod)
            db.session.commit()

    except:
        return json.dumps({"ERROR": "Problem in Adding a Product"})
    else:
        return json.dumps(({"SUCCESS": "Product Added Successfully.."}))
    #return "Post method Invoked"


#  http://localhost:5000/api/v1/product/{id}  ---> put-- {request body}
@app.route('/api/v1/product/<int:pid>', methods=['PUT'])   # agara ek hi body update krna ho to pTCH USE HOTA HAI
@jwt_required()
def update_product_information(pid):

    db_product = Product.query.filter_by(id=pid).first()
    if db_product:
        req_data = request.get_json()

        MANDATORY_FIELD = ["PRODUCT_NAME", "PRODUCT_QYT", "PRODUCT_PRICE", "PRODUCT_CATEGORY", "PRODUCT_VENDOR"]

        keys = req_data.keys()
        print(keys)
        for mfield in MANDATORY_FIELD:
            if mfield not in keys:
                return json.dumps({"ERROR": f"{mfield} field id missing"})

        db_product.name = req_data.get('PRODUCT_NAME')
        db_product.qyt = req_data.get('PRODUCT_QYT')
        db_product.price = req_data.get('PRODUCT_PRICE')
        db_product.vendor = req_data.get('PRODUCT_VENDOR')
        db_product.category = req_data.get('PRODUCT_CATEGORY')
        #with app.app_context():
        db.session.commit()
        return json.dumps(({"SUCCESS": "Product Updated Successfully.."}))

    else:
        return json.dumps({"ERROR": "Product with Given ID Cannot Be Updated/ Found"})


@app.route('/api/v1/product/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    db_product = Product.query.filter_by(id=pid).first()
    if db_product:
        #with app.app_context():
        db.session.delete(db_product)
        db.session.commit()
        return json.dumps(({"SUCCESS": "Product removed Successfully.."}))

    else:
        return json.dumps({"ERROR": "Product with Given ID Cannot Be deleted/ Found"})
