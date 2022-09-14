from base64 import encode
from hashlib import algorithms_available
from flask_jwt_extended import create_access_token,get_jwt_identity


class JWT_handler():
    def makeToken(self,data):
        return create_access_token(data)
    def readToken(self):
        return get_jwt_identity()
