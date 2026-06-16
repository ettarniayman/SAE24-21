from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length


class NewsletterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("Prénom", validators=[Optional(), Length(max=80)])
    submit = SubmitField("S'inscrire")
