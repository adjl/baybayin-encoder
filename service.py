#!/usr/bin/env python3

import os.path

import app.app

from bottle import request
from bottle import route
from bottle import run
from bottle import static_file


@route('/')
def index():
    return static_file('index.html', root='static_files')


@route('/', method='post')
def index_post():
    return ''.join(map(str, app.app.transform(request.forms.get('input'))))


@route('/fonts/<font_name:re:[a-zA-Z]+>.ttf')
def baybayin_ttf(font_name):
    filename = 'fonts/' + font_name + '.ttf'
    return static_file(filename, root='static_files')


run(host='localhost', port=8080, debug=True)
