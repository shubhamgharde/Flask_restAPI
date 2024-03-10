from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_TRACK_MODFICATION'] =False
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/rest_db'
db = SQLAlchemy(app)

# yahase jaisehi token mil jayega to kya return kar dunga mai
# return json.dumps({"ERROR": "Invalid Credentials...!"})  iske alawa jsonify b ek object hota hai
# 400 ya 401 status code hai,client side error, unauthorized
#token configure hone ke liye sabse pehele kya hona chahiye