#!/bin/python3
# 載入Flask套件
from flask import Flask,jsonify, render_template
from flask_restful import Api
from common.JWT_handler import JWT_handler
from flask_jwt_extended import  JWTManager,jwt_required
'''--------------------------------------
    import api所提供的resouce file
---------------------------------------'''
from resource.index import test
from resource.User import User
from resource.Users import Users
from resource.login_handler import login_handler
from resource.ProgrammingRequest import ProgrammingRequest
from resource.course import course
from resource.ProgrammingTest_without_hardware import ProgrammingTest_without_hardware


app = Flask(__name__)
jwt=JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'test' 
app.config['JWT_TOKEN_LOCATION']=['headers','cookies']
app.config['JWT_ACCESS_COOKIE_NAME']="access_token_cookie"
'''
Api要提供的resource放在resource
'''
api = Api(app)
api.add_resource(User, "/api/User")
api.add_resource(Users, "/api/Users")
api.add_resource(login_handler,"/api/login")
api.add_resource(ProgrammingRequest,"/api/ProgrammingRequest")
api.add_resource(course,"/api/course")
api.add_resource(ProgrammingTest_without_hardware,"/api/ProgrammingRequest_without_hardware")
if __name__ == "__main__":
    app.run(port=8087,debug=True)