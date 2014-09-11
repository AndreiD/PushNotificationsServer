# -*- coding: utf-8 -*-

from app import *
from wtforms.validators import Required, Length
from wtforms import Form, TextField, TextAreaField


class SendPushNotificationsForm(Form):

    payload = TextAreaField('data',  default="{'the_message': 'You have x new friends', 'param2': 'value2'}", validators=[Length(max=1024, message='max 1024 characters')])
    category = TextField('category', default="all",  validators=[Required(), Length(max=255, message='max 255 characters')])




