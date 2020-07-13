import os
import sys

from flask import Flask
from pyfladesk import init_gui


def resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = Flask(__name__, static_url_path="", static_folder=resource_path(
    'static'), template_folder=resource_path("templates"))


from routes import *


def main():
    init_gui(app, port=2088, width=1200, height=705,
             window_title=" ", icon="./static/icon/palmcat.png", argv=None)


if __name__ == '__main__':
    main()
