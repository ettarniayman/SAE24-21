from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class BookingForm(FlaskForm):
    first_name = StringField("Prénom", validators=[DataRequired(), Length(1, 80)])
    last_name = StringField("Nom", validators=[DataRequired(), Length(1, 80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=200)])
    phone = StringField("Téléphone", validators=[Optional(), Length(max=30)])
    nationality = StringField("Nationalité", validators=[Optional(), Length(max=80)])
    participants = IntegerField("Nombre de participants", validators=[DataRequired(), NumberRange(min=1, max=50)], default=1)
    departure_date = DateField("Date de départ souhaitée", validators=[DataRequired()])
    return_date = DateField("Date de retour estimée", validators=[Optional()])
    special_requests = TextAreaField("Demandes spéciales / Remarques", validators=[Optional(), Length(max=2000)])
    honeypot = StringField("Ne pas remplir")
    submit = SubmitField("Envoyer ma demande de réservation")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if self.honeypot.data:
            return False
        return True
