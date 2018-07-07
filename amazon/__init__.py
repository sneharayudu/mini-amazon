from flask import Flask


app = Flask('amazon')
app.secret_key = 'some_key'

from amazon import api

