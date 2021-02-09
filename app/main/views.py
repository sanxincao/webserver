from datetime import datetime
from flask import render_template,session,redirect,url_for
#session ?sessions
from . import main
from .forms import nameform
from .. import db
from ..models import User