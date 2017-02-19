from flask import Flask

app = Flask(__name__)
from app import views
from app import authentication
from app import resolution
from app import group
