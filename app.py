#!/usr/bin/env python3

from bottle import request
from bottle import route
from bottle import run
from bottle import static_file


@route('/')
def index():
    return static_file('index.html', root='.')


@route('/', method='post')
def index_post():
    return request.forms.get('input')


run(host='localhost', port=8080, debug=True)
