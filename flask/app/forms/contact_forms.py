from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    first_name = StringField("Prénom", validators=[DataRequired(), Length(1, 80)])
    last_name = StringField("Nom", validators=[DataRequired(), Length(1, 80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=200)])
    phone = StringField("Téléphone", validators=[Optional(), Length(max=30)])
    destination_interest = StringField("Destination souhaitée", validators=[Optional(), Length(max=150)])
    subject = SelectField("Sujet", choices=[
        ("", "— Choisissez un sujet —"),
        ("information", "Demande d'information"),
        ("devis", "Demande de devis"),
        ("reservation", "Réservation"),
        ("reclamation", "Réclamation"),
        ("partenariat", "Partenariat"),
        ("autre", "Autre"),
    ], validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=3000)])
    honeypot = StringField("Ne pas remplir")
    submit = SubmitField("Envoyer le message")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if self.honeypot.data:
            return False
        return True
