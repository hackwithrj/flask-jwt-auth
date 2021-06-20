from flask import Flask,request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.config.from_object('config.Config')

@app.route('/', methods=["GET"])
def index():
    return 'Hello World'

@app.route("/api/auth/login", methods=["POST"])
def login():
    """
    Login with username and password
    
    Returns:
        Json with access token and refresh token
    """
    req = request.get_json()
    user_name = req["user_name"]
    password = req["password"]
    if user_name == None or password == None:
        return jsonify({"msg": "Enter the values"}), 400
    elif user_name != app.config.get("USER_NAME") or password != app.config.get("PASSWORD"):
        return jsonify({"msg": "Wrong username or password"}), 401
    else:
        access_token = create_access_token(identity=user_name, fresh=True) # change default fresh to true for access token
        refresh_token = create_refresh_token(identity=user_name)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Login with refresh token
    
    Returns:
        Json with access token with fresh parameter as false
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@app.route("/api/user",methods=["GET"])
@jwt_required(fresh=False)      # allow refresh token 
def get_users():
    """
    Api which is accessible for access token which is not fresh
    
    Returns:
        Json with user name
    """
    return jsonify({"name":app.config.get("USER_NAME")})

@app.route("/api/transaction",methods=["GET"])
@jwt_required(fresh=True)      # won't allow refresh token only jwt is allowed
def get_transactions():
    """
    Critical Api which is accessible for only fresh access token
    
    Returns:
        Json with user name and password
    """
    return jsonify({"name":app.config.get("USER_NAME"),"password":app.config.get("password")})


if __name__ == "__main__":
    app.run(debug=True)
