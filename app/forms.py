from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

class GetToken(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Lagre')

class MyToken():
    def __init__(self):
        pass

    def set_token(self, aToken):
        self.token = aToken
    
    def get_token(self):
        return self.token