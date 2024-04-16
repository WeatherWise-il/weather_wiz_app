from wtforms import StringField
from wtforms import SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField


class get_weather_form(FlaskForm):
    search_term = StringField('Search:', render_kw={'hx-get': '/search', 'hx-target': '#select_field', 
                                                    'hx-trigger': 'keyup delay:500ms',
                                                    },validators=[InputRequired()])
    
                                                    
    select_field = SelectField('Select:',  id='select_field', default="None",validators=[DataRequired()])

    
    
    