import os
import sys
import auto_py_to_exe
import routes

from flask import Flask
from PyQt5 import QtWebEngine, QtWebEngineCore
from pyfladesk import init_gui


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# if getattr(sys, 'frozen', False):
#     template_folder = resource_path('templates')
#     static_folder = resource_path('static')
#     app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
# else:
#     app = Flask(__name__)

app = Flask(__name__, static_url_path="", static_folder=resource_path(
    'static'), template_folder=resource_path("templates"))

from routes import *


def main():
    init_gui(app, port=2020, width=1200, height=700,
             window_title=" ", icon="C:/Program Files (x86)/pero USP/palmcat.png", argv=None)


if __name__ == '__main__':
    main()
