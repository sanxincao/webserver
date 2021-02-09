from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from flask_bootstrap import Bootstrap
from config import config

class SQLAlchemy(_BaseSQLAlchemy):
     def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True

db=SQLAlchemy()
bootstrap=Bootstrap()
def Create_app(configname):
  app=Flask(__name__)
  app.config.from_object(config[configname])
  config[configname].init_app(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  bootstrap.init_app(app)
  db.init_app(app)
  return app