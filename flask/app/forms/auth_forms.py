from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class LoginForm(FlaskForm):
    identifier = StringField("Email ou nom d'utilisateur", validators=[DataRequired(), Length(3, 150)])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")


class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(3, 80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=200)])
    first_name = StringField("Prénom", validators=[Length(max=80)])
    last_name = StringField("Nom", validators=[Length(max=80)])
    phone = StringField("Téléphone", validators=[Length(max=20)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Créer mon compte")


class ProfileForm(FlaskForm):
    first_name = StringField("Prénom", validators=[Optional(), Length(max=80)])
    last_name = StringField("Nom", validators=[Optional(), Length(max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=200)])
    phone = StringField("Téléphone", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Enregistrer")
