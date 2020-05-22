import os
import sys

from flask import Flask
from pyfladesk import init_gui


def resource_path(relative_path):
    ''' Get absolute path to resource, works for dev and for PyInstaller '''
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

from routes import *


def main():
    init_gui(app, port=1234, width=1200, height=700,
             window_title=" ", icon="C:\\project\\pero_USP\\static\\icon\\palmcat.png", argv=None)


if __name__ == '__main__':
    main()
