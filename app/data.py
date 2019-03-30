# data.py
from flask import Blueprint
app = Blueprint("data", __name__,
    static_url_path='/data', static_folder='./data'
)
