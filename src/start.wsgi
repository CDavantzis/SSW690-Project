#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app import flask_app as application

sys.stdout = sys.stderr
