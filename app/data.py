# data.py
from flask import Blueprint
app = Blueprint("data2", __name__,
    static_url_path='/data2', static_folder='./data2'
)
