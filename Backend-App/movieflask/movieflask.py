# -*- coding:utf8 -*-
import time
from flask import Flask,g,request,render_template,request,flash,url_for,make_response,g
from database.movieDB import MovieModule

movieapp = Flask(__name__)
movieapp.secret_key = 'some_secret'



@movieapp.before_request
def before_request():
    g.db = MovieModule()

# @movieapp.teardown_request
# def teardown_request(exception):
#     if hasattr(g, 'db'):
#         g.db.disconnect()

@movieapp.route('/', methods = ['GET', 'POST'] )
def index():
    result = g.db.search_name("我的战争")
    return make_response('')


@movieapp.route('/search')
def search():

    return make_response('AAAA')
def startmovie(port):
    movieapp.run(host='0.0.0.0',port=port)