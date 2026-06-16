from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SelectField, BooleanField,
    IntegerField, DecimalField, SubmitField, DateField, DateTimeField, PasswordField
)
from wtforms.validators import DataRequired, Optional, Length, NumberRange, Email


class DestinationForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=120)])
    name_en = StringField("Nom (EN)", validators=[Optional(), Length(max=120)])
    slug = StringField("Slug URL", validators=[Optional(), Length(max=120)])
    country_id = SelectField("Pays", coerce=int, validators=[DataRequired()])
    region = StringField("Région", validators=[Optional(), Length(max=100)])
    short_desc_fr = TextAreaField("Description courte (FR)", validators=[Optional()])
    short_desc_en = TextAreaField("Description courte (EN)", validators=[Optional()])
    long_desc_fr = TextAreaField("Description longue (FR)", validators=[Optional()])
    long_desc_en = TextAreaField("Description longue (EN)", validators=[Optional()])
    history_fr = TextAreaField("Histoire (FR)", validators=[Optional()])
    culture_fr = TextAreaField("Culture (FR)", validators=[Optional()])
    gastronomy_fr = TextAreaField("Gastronomie (FR)", validators=[Optional()])
    latitude = DecimalField("Latitude", validators=[Optional()], places=7)
    longitude = DecimalField("Longitude", validators=[Optional()], places=7)
    average_budget_eur = IntegerField("Budget moyen (EUR/jr)", validators=[Optional()])
    difficulty_level = SelectField("Difficulté", choices=[
        ("easy", "Facile"), ("moderate", "Modéré"), ("hard", "Difficile")
    ])
    safety_level = SelectField("Sécurité", choices=[
        ("safe", "Sûr"), ("moderate", "Modéré"), ("caution", "Prudence")
    ])
    best_period_fr = StringField("Meilleure période (FR)", validators=[Optional(), Length(max=200)])
    climate_fr = TextAreaField("Climat (FR)", validators=[Optional()])
    destination_type = SelectField("Type", choices=[
        ("city", "Ville"), ("nature", "Nature"), ("desert", "Désert"),
        ("mountain", "Montagne"), ("beach", "Plage"), ("historical", "Historique"),
    ])
    image_main = FileField("Image principale", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp"])])
    video_url = StringField("URL Vidéo", validators=[Optional(), Length(max=500)])
    youtube_id = StringField("ID YouTube", validators=[Optional(), Length(max=50)])
    street_view_lat = DecimalField("Street View Lat", validators=[Optional()], places=7)
    street_view_lng = DecimalField("Street View Lng", validators=[Optional()], places=7)
    meta_title_fr = StringField("Meta Title (FR)", validators=[Optional(), Length(max=200)])
    meta_desc_fr = TextAreaField("Meta Description (FR)", validators=[Optional(), Length(max=300)])
    is_featured = BooleanField("Mise en avant")
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Enregistrer")


class HotelForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(), Length(max=150)])
    slug = StringField("Slug URL", validators=[Optional(), Length(max=150)])
    destination_id = SelectField("Destination", coerce=int, validators=[DataRequired()])
    hotel_type = SelectField("Type", choices=[
        ("hotel", "Hôtel"), ("riad", "Riad"), ("villa", "Villa"),
        ("resort", "Resort"), ("hostel", "Auberge"), ("apartment", "Appartement"),
    ])
    stars = IntegerField("Étoiles (1-5)", validators=[Optional(), NumberRange(1, 5)])
    address = StringField("Adresse", validators=[Optional(), Length(max=300)])
    latitude = DecimalField("Latitude", validators=[Optional()], places=7)
    longitude = DecimalField("Longitude", validators=[Optional()], places=7)
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    price_min = DecimalField("Prix min (EUR)", validators=[Optional()], places=2)
    price_max = DecimalField("Prix max (EUR)", validators=[Optional()], places=2)
    has_pool = BooleanField("Piscine")
    has_spa = BooleanField("Spa")
    has_restaurant = BooleanField("Restaurant")
    has_wifi = BooleanField("WiFi", default=True)
    booking_url = StringField("Lien de réservation", validators=[Optional(), Length(max=500)])
    is_partner = BooleanField("Partenaire")
    is_featured = BooleanField("Mise en avant")
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class ProgramForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=200)])
    name_en = StringField("Nom (EN)", validators=[Optional(), Length(max=200)])
    slug = StringField("Slug URL", validators=[Optional(), Length(max=150)])
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    duration_days = IntegerField("Durée (jours)", validators=[DataRequired(), NumberRange(1, 365)])
    price_per_person = DecimalField("Prix/personne (EUR)", validators=[Optional()], places=2)
    price_per_person_discounted = DecimalField("Prix réduit (EUR)", validators=[Optional()], places=2)
    theme = SelectField("Thème", choices=[
        ("", "— Aucun —"), ("culture", "Culture"), ("adventure", "Aventure"),
        ("nature", "Nature"), ("luxury", "Luxe"), ("sport", "Sport"),
        ("gastronomy", "Gastronomie"), ("family", "Famille"), ("football", "Football"),
    ])
    difficulty = SelectField("Difficulté", choices=[
        ("easy", "Facile"), ("moderate", "Modéré"), ("hard", "Difficile")
    ])
    includes_fr = TextAreaField("Inclus (FR)", validators=[Optional()])
    excludes_fr = TextAreaField("Non inclus (FR)", validators=[Optional()])
    departure_city = StringField("Ville de départ", validators=[Optional(), Length(max=100)])
    is_featured = BooleanField("Mise en avant")
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class BlogPostForm(FlaskForm):
    title_fr = StringField("Titre (FR)", validators=[DataRequired(), Length(max=250)])
    title_en = StringField("Titre (EN)", validators=[Optional(), Length(max=250)])
    slug = StringField("Slug URL", validators=[Optional(), Length(max=200)])
    category_id = SelectField("Catégorie", coerce=int, validators=[Optional()])
    excerpt_fr = TextAreaField("Extrait (FR)", validators=[Optional()])
    content_fr = TextAreaField("Contenu (FR)", validators=[DataRequired()])
    content_en = TextAreaField("Contenu (EN)", validators=[Optional()])
    meta_title_fr = StringField("Meta Title", validators=[Optional(), Length(max=200)])
    meta_desc_fr = TextAreaField("Meta Description", validators=[Optional(), Length(max=300)])
    is_featured = BooleanField("Mise en avant")
    is_published = BooleanField("Publier")
    submit = SubmitField("Enregistrer")


class AirlineForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(), Length(max=100)])
    slug = StringField("Slug", validators=[Optional(), Length(max=80)])
    iata_code = StringField("Code IATA", validators=[Optional(), Length(max=5)])
    website = StringField("Site web", validators=[Optional(), Length(max=300)])
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    is_partner = BooleanField("Partenaire", default=True)
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class PromotionForm(FlaskForm):
    title_fr = StringField("Titre (FR)", validators=[DataRequired(), Length(max=200)])
    title_en = StringField("Titre (EN)", validators=[Optional(), Length(max=200)])
    slug = StringField("Slug", validators=[Optional(), Length(max=150)])
    destination_id = SelectField("Destination", coerce=int, validators=[Optional()])
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    original_price = DecimalField("Prix original (EUR)", validators=[Optional()], places=2)
    promo_price = DecimalField("Prix promo (EUR)", validators=[Optional()], places=2)
    discount_percent = IntegerField("Réduction (%)", validators=[Optional(), NumberRange(0, 100)])
    promo_code = StringField("Code promo", validators=[Optional(), Length(max=30)])
    valid_from = DateTimeField("Valide du", format="%Y-%m-%dT%H:%M", validators=[Optional()])
    valid_until = DateTimeField("Valide jusqu'au", format="%Y-%m-%dT%H:%M", validators=[Optional()])
    promo_type = SelectField("Type", choices=[
        ("general", "Général"), ("flight", "Vol"), ("hotel", "Hôtel"),
        ("package", "Package"), ("activity", "Activité"),
    ])
    is_active = BooleanField("Active", default=True)
    is_featured = BooleanField("Mise en avant")
    submit = SubmitField("Enregistrer")


class FAQForm(FlaskForm):
    category_id = SelectField("Catégorie", coerce=int, validators=[DataRequired()])
    question_fr = TextAreaField("Question (FR)", validators=[DataRequired()])
    question_en = TextAreaField("Question (EN)", validators=[Optional()])
    answer_fr = TextAreaField("Réponse (FR)", validators=[DataRequired()])
    answer_en = TextAreaField("Réponse (EN)", validators=[Optional()])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Enregistrer")


class TestimonialForm(FlaskForm):
    client_name = StringField("Nom du client", validators=[DataRequired(), Length(max=100)])
    client_country = StringField("Pays du client", validators=[Optional(), Length(max=80)])
    rating = SelectField("Note", coerce=int, choices=[(i, f"{i}/5") for i in range(1, 6)], validators=[DataRequired()])
    title = StringField("Titre", validators=[Optional(), Length(max=200)])
    comment = TextAreaField("Commentaire", validators=[DataRequired()])
    destination_id = SelectField("Destination", coerce=int, validators=[Optional()])
    is_approved = BooleanField("Approuvé")
    is_featured = BooleanField("Mise en avant")
    submit = SubmitField("Enregistrer")


class UserForm(FlaskForm):
    role = SelectField("Rôle", choices=[
        ("client", "Client"), ("agent", "Agent Voyage"),
        ("admin", "Administrateur"), ("super_admin", "Super Administrateur"),
    ])
    is_active = BooleanField("Actif", default=True)
    password = PasswordField("Nouveau mot de passe (laisser vide pour ne pas changer)", validators=[Optional(), Length(min=8)])
    submit = SubmitField("Enregistrer")


class ShopProductForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=150)])
    name_en = StringField("Nom (EN)", validators=[Optional(), Length(max=150)])
    slug = StringField("Slug", validators=[Optional(), Length(max=150)])
    category_id = SelectField("Catégorie", coerce=int, validators=[Optional()])
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    price = DecimalField("Prix (EUR)", validators=[DataRequired()], places=2)
    price_discounted = DecimalField("Prix réduit (EUR)", validators=[Optional()], places=2)
    stock = IntegerField("Stock", validators=[Optional()])
    affiliate_url = StringField("URL Affilié", validators=[Optional(), Length(max=500)])
    is_affiliate = BooleanField("Produit affilié")
    is_featured = BooleanField("Mise en avant")
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class RSSItemForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired(), Length(max=300)])
    link = StringField("Lien URL", validators=[Optional(), Length(max=500)])
    description = TextAreaField("Description", validators=[Optional()])
    category = SelectField("Catégorie", choices=[
        ("news", "Actualité"), ("destination", "Destination"),
        ("promotion", "Promotion"), ("article", "Article"), ("partner", "Partenaire"),
    ])
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class CountryForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=100)])
    name_en = StringField("Nom (EN)", validators=[DataRequired(), Length(max=100)])
    code = StringField("Code ISO 3", validators=[DataRequired(), Length(min=2, max=3)])
    continent = StringField("Continent", validators=[Optional(), Length(max=50)])
    capital = StringField("Capitale", validators=[Optional(), Length(max=100)])
    currency = StringField("Monnaie", validators=[Optional(), Length(max=50)])
    flag_emoji = StringField("Emoji drapeau", validators=[Optional(), Length(max=10)])
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")


class ActivityForm(FlaskForm):
    name_fr = StringField("Nom (FR)", validators=[DataRequired(), Length(max=150)])
    name_en = StringField("Nom (EN)", validators=[Optional(), Length(max=150)])
    slug = StringField("Slug", validators=[Optional(), Length(max=120)])
    category_id = SelectField("Catégorie", coerce=int, validators=[Optional()])
    description_fr = TextAreaField("Description (FR)", validators=[Optional()])
    price_per_person = DecimalField("Prix/personne (EUR)", validators=[Optional()], places=2)
    duration_hours = DecimalField("Durée (heures)", validators=[Optional()], places=1)
    activity_type = SelectField("Type d'activité", choices=[
        ("monument", "Monument"), ("stadium", "Stade"), ("museum", "Musée"),
        ("medina", "Médina"), ("desert", "Désert"), ("mountain", "Montagne"),
        ("hike", "Randonnée"), ("beach", "Plage"), ("surf", "Surf"),
        ("nautical", "Nautique"), ("family", "Famille"), ("sport", "Sport"),
        ("cultural", "Culturel"), ("luxury", "Luxe"), ("excursion", "Excursion"),
    ])
    is_featured = BooleanField("Mise en avant")
    is_active = BooleanField("Actif", default=True)
    submit = SubmitField("Enregistrer")
