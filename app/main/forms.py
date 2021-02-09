from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class nameform(FlaskForm):

  name=StringField('name',validators=[DataRequired()])
  submit=SubmitField('submit')