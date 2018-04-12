from .load_data import calc

from flask import Flask

app = Flask(__name__,
            static_folder='../web/static',
            static_url_path='/static',
            template_folder='../web/templates')

from .view import *

