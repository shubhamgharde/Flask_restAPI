from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, get_jwt_identity, jwt_required
from flask import Flask
from datetime import datetime
from datetime import timedelta
from datetime import timezone

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '1287A2^#&Dsb(@sdvhrtefwet' #token configure hone ke liye sabse pehele kya hona chahiye
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=15)
jwt = JWTManager(app)
from flask import request, jsonify
import json



#http://localhost:5000/gettoken
#sabse pehele username password send krna pdega to uske liye


@app.route('/gettoken',methods=['POST'])
def validate_user():
    req_body = request.get_json()
    if req_body.get('USERNAME') == 'admin' and req_body.get('PASSWORD') == 'root123':
        atoken = create_access_token(identity=(req_body.get('USERNAME'), req_body.get('PASSWORD')))
        rtoken = create_refresh_token(identity=(req_body.get('USERNAME'), req_body.get('PASSWORD')))
        return json.dumps({"access_token": atoken, "refresh_token": rtoken})    #yahase jaisehi token mil jayega to kya return kar dunga mai
    else:
        return jsonify('Invalid credentials...!'), 401
        #return json.dumps({"ERROR": "Invalid Credentials...!"})  iske alawa jsonify b ek object hota hai
        # 400 ya 401 status code hai,client side error, unauthorized



#http://localhost:5000/public/api
@app.route('/public/api', methods=['GET'])
def public_api_endpont():
    return json.dumps({"SUCCESS": "Public API Is INVOKED"})


#http://localhost:5000/secure/api
@app.route('/secure/api', methods=['GET'])
@jwt_required()
def secured_api_endpoint():
    return json.dumps({"SUCCESS": "Secured API is Invoked...!"})


@app.route('/refresh/api', methods=['GET'])
@jwt_required(refresh=True) #refresh token dena hai--request krna hai
def get_accesstoken_using_refreshtoken():    #return me kya dega ---access token---responce me
    identity = get_jwt_identity()   #username pass nahi hai isliye ye pass kiya hai
    atoken = create_access_token(identity=identity)
    return json.dumps({"access_token": atoken})


if __name__=='__main__':
    app.run(debug=True)


